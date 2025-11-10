# Retell Web Call 集成技术文档

## 📋 文档概述

本文档详细描述了 intake phone agent 如何集成 Retell AI 平台来启动和管理 web call（网页端语音通话）的完整技术设计。适用于需要在其他项目中参考或复用此设计的开发团队。

**版本**: v1.0  
**日期**: 2025-11-10  
**作者**: Minerva Team  

---

## 🏗️ 架构概述

### 系统组件关系图

```
┌─────────────────┐
│   前端应用      │
│  (Web Browser)  │
└────────┬────────┘
         │ 1. POST /intake/create-web-call
         │    {patient_id: "123"}
         ▼
┌─────────────────────────────────────────┐
│          FastAPI Backend                │
│  ┌────────────────────────────────────┐ │
│  │  Router (router.py)                │ │
│  │  - /intake/create-web-call         │ │
│  └──────────┬─────────────────────────┘ │
│             │                            │
│             ▼                            │
│  ┌────────────────────────────────────┐ │
│  │  Service (service.py)              │ │
│  │  - create_intake_web_call()        │ │
│  └──────────┬─────────────────────────┘ │
│             │                            │
│             ▼                            │
│  ┌────────────────────────────────────┐ │
│  │  Retell API Layer                  │ │
│  │  - create_web_call()               │ │
│  │  - update_llm_prompt()             │ │
│  └──────────┬─────────────────────────┘ │
└─────────────┼─────────────────────────────┘
              │ 2. API Call
              ▼
┌──────────────────────────────────────────┐
│        Retell AI Platform                │
│  - Agent Management                      │
│  - LLM Configuration                     │
│  - Web Call Infrastructure               │
└──────────────┬───────────────────────────┘
               │ 3. Return access_token
               │
               ▼
┌──────────────────────────────────────────┐
│          Frontend Integration            │
│  - Retell Web SDK                        │
│  - RetellWebClient                       │
│  - Audio/Video Streaming                 │
└──────────────────────────────────────────┘
```

### 核心技术栈

- **后端框架**: FastAPI (Python)
- **AI 平台**: Retell AI
- **Retell SDK**: `retell-sdk` (Python)
- **前端 SDK**: `@retell-ai/retell-client-js-sdk`
- **数据存储**: CSV (可扩展为数据库)
- **LLM**: OpenAI GPT-4o (用于生成 summary 和 evaluation)

---

## 🔑 核心组件详解

### 1. API 端点 (router.py)

#### 1.1 创建 Web Call 端点

**端点**: `POST /intake/create-web-call`

**功能**: 为患者创建一个 web call 会话，返回前端所需的 access token 和相关信息。

**请求参数**:
```json
{
  "patient_id": "123456789",           // 可选，患者ID
  "previous_transcript": [             // 可选，用于恢复中断的通话
    {
      "role": "agent",
      "content": "Hello, how are you?"
    },
    {
      "role": "user",
      "content": "I'm fine, thank you."
    }
  ]
}
```

**响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "call_id": "call_abc123xyz456",
  "agent_id": "agent_e0582ed7942755487668942253",
  "patient_name": "Julia Liu",
  "message": "Web call created successfully"
}
```

**关键代码**:
```python
@intake_router.post("/create-web-call")
async def create_web_call_endpoint(
    request: Request,
    db: Optional[AsyncSession] = Depends(get_db_session)
):
    """创建 intake web call"""
    body = await request.json() if request.headers.get('content-type') == 'application/json' else {}
    patient_id = body.get('patient_id')
    previous_transcript = body.get('previous_transcript')
    
    # 使用默认测试患者（如果未提供）
    if not patient_id:
        patient_id = "123456789"
        logging.info(f"==== 使用默认测试 patient_id: {patient_id}")
    
    result = await create_intake_web_call(
        patient_id=patient_id,
        db=db,
        previous_transcript=previous_transcript
    )
    
    if result.get('status_code') == 200:
        return JSONResponse(
            status_code=200,
            content=result.get('content', {})
        )
    else:
        raise HTTPException(
            status_code=result.get('status_code', 500),
            detail=result.get('content', {}).get('message', 'Failed to create web call')
        )
```

---

### 2. 业务逻辑层 (service.py)

#### 2.1 create_intake_web_call 函数

这是创建 web call 的核心函数，负责：
1. 获取患者信息
2. 准备动态变量（patient info, visit info 等）
3. 更新 LLM prompt（个性化对话内容）
4. 调用 Retell API 创建 web call

**完整代码流程**:

```python
async def create_intake_web_call(
    patient_id: Optional[str] = None,
    db: Optional[Any] = None,
    previous_transcript: Optional[list] = None
) -> Dict[str, Any]:
    """
    创建 intake web call
    
    步骤：
    1. 获取患者信息（从 UC API 或使用默认数据）
    2. 获取即将到来的预约信息
    3. 准备动态变量（用于 LLM prompt 填充）
    4. 更新 LLM 的 begin_message 和 general_prompt
    5. 调用 Retell API 创建 web call
    6. 返回 access_token 和 call_id
    """
    
    logging.info(f"==== 创建 intake web call, patient_id: {patient_id}")
    
    # 步骤 1: 获取患者信息
    patient_info = None
    if patient_id:
        try:
            patient_client = PatientClient()
            patient_info = patient_client.get_patient_info(patient_id)
            
            if not patient_info or not patient_info.patient_id:
                # 未找到患者，使用占位数据
                patient_info = PatientInfo(
                    patient_id=patient_id,
                    patient_name=f"Patient {patient_id[:8]}",
                    phone_number="",
                    timezone="US/Pacific"
                )
        except Exception as e:
            logging.error(f"==== 获取患者信息失败: {e}")
            # 使用占位数据
            patient_info = PatientInfo(
                patient_id=patient_id,
                patient_name=f"Patient {patient_id[:8]}",
                phone_number="",
                timezone="US/Pacific"
            )
    else:
        # 使用默认测试数据
        patient_id = DEFAULT_TEST_PATIENT_ID
        patient_info = PatientInfo(
            patient_id=DEFAULT_TEST_PATIENT_ID,
            patient_name=DEFAULT_TEST_PATIENT_NAME,
            phone_number="",
            timezone="US/Pacific"
        )
    
    # 步骤 2: 提取患者姓名组件
    patient_name = patient_info.patient_name
    patient_name_parts = patient_name.strip().split()
    patient_first_name = patient_name_parts[0] if patient_name_parts else ""
    patient_last_name = " ".join(patient_name_parts[1:]) if len(patient_name_parts) > 1 else ""
    
    # 步骤 2.5: 获取即将到来的预约信息和营养师姓名
    patient_timezone = patient_info.timezone or "US/Pacific"
    upcoming_visit_info, appointment_dietitian_name = await get_upcoming_visit_info(
        patient_info.patient_id, 
        patient_timezone
    )
    
    # 确定营养师姓名（优先使用预约中的营养师）
    DEFAULT_DIETITIAN_NAME = "Nina"
    dietician_name = appointment_dietitian_name if appointment_dietitian_name else DEFAULT_DIETITIAN_NAME
    
    # 步骤 3: 准备动态变量
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dynamic_variables = {
        "patient_id": patient_info.patient_id,
        "patient_first_name": patient_first_name,
        "patient_last_name": patient_last_name,
        "patient_name": patient_name,
        "patient_dob": patient_info.dob,
        "patient_timezone": patient_timezone,
        "doctor_name": patient_info.doctor_name,
        "assigned_rd_name": dietician_name,
        "dietician_name": dietician_name,
        "clinic_name": patient_info.business_name,
        "current_date_time": current_datetime,
        "timezone": patient_timezone,
        "upcoming_visit_info": upcoming_visit_info,
        "previous_conversation": ""
    }
    
    # 添加历史对话记录（用于恢复中断的通话）
    if previous_transcript and len(previous_transcript) > 0:
        transcript_text = "\n".join([
            f"{msg.get('role', 'unknown').upper()}: {msg.get('content', '')}"
            for msg in previous_transcript
        ])
        dynamic_variables["previous_conversation"] = transcript_text
        logging.info(f"==== 恢复通话，包含 {len(previous_transcript)} 条历史消息")
    
    # 步骤 3.5: 更新 LLM 的 begin_message 和 general_prompt
    agent_id = INTAKE_AGENT_ID  # "agent_e0582ed7942755487668942253"
    llm_id = INTAKE_LLM_ID      # "llm_3400cedfe3528e616f844c0cdb50"
    
    try:
        # 加载模板并填充动态变量
        begin_message_template = intake_begin_message_template()
        prompt_template = intake_prompt_template()
        
        # 转换模板中的双大括号 {{var}} 为单大括号 {var}
        begin_message_single = convert_double_braces_to_single(begin_message_template)
        prompt_single = convert_double_braces_to_single(prompt_template)
        
        # 使用 safe_format 填充变量
        begin_message = safe_format(begin_message_single, dynamic_variables)
        general_prompt = safe_format(prompt_single, dynamic_variables)
        
        # 推送到 Retell LLM
        update_llm_begin_message_and_prompt(
            llm_id=llm_id,
            begin_message=begin_message,
            general_prompt=general_prompt
        )
        logging.info("==== 已更新 LLM 的 begin_message 和 general_prompt")
    except Exception as e:
        logging.error(f"==== 更新 LLM prompt 失败: {e}", exc_info=True)
    
    # 步骤 4: 创建 web call
    metadata = {
        "patient_id": patient_info.patient_id,
        "patient_name": patient_name,
        "doctor_name": patient_info.doctor_name,
        "clinic_name": patient_info.business_name,
        "call_type": "intake_web_call"
    }
    
    response = create_web_call(
        agent_id=agent_id,
        metadata=metadata,
        retell_llm_dynamic_variables=dynamic_variables
    )
    
    if response.get('status_code') == 200:
        web_call_response = response.get('content')
        
        access_token = web_call_response.get('access_token')
        call_id = web_call_response.get('call_id')
        
        logging.info(f"==== Web call 创建成功: {call_id}")
        
        return {
            "status_code": 200,
            "content": {
                "access_token": access_token,
                "call_id": call_id,
                "agent_id": agent_id,
                "patient_name": patient_name,
                "message": "Web call created successfully"
            }
        }
    else:
        logging.error(f"==== Web call 创建失败: {response.get('content')}")
        return {
            "status_code": 500,
            "content": response.get('content', {"message": "Failed to create web call"})
        }
```

**关键点**：
- **动态变量注入**: 所有患者信息通过 `retell_llm_dynamic_variables` 传递给 Retell
- **Prompt 个性化**: 每次通话前都会更新 LLM 的 prompt，确保 AI 使用正确的患者姓名、预约信息等
- **错误处理**: 完善的降级策略，API 失败时使用默认数据，确保服务可用

---

### 3. Retell API 封装层

#### 3.1 创建 Web Call (retell_api/api.py)

```python
def create_web_call(
    agent_id: str,
    metadata: Optional[Dict[str, Any]] = None,
    retell_llm_dynamic_variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    使用 Retell SDK 创建 web call
    
    Args:
        agent_id: Retell Agent ID（在 Retell 平台配置）
        metadata: 元数据（用于 webhook 回调识别）
        retell_llm_dynamic_variables: LLM 动态变量（用于 prompt 填充）
    
    Returns:
        {
            "status_code": 200,
            "content": {
                "access_token": "...",
                "call_id": "...",
                "agent_id": "..."
            }
        }
    """
    logging.info('==== 创建 web call, agent_id: %s', agent_id)
    
    try:
        retell = get_retell_client()
        web_call_response = retell.call.create_web_call(
            agent_id=agent_id,
            metadata=metadata or {},
            retell_llm_dynamic_variables=retell_llm_dynamic_variables or {}
        )
        
        # 提取 access_token 和 call_id
        if hasattr(web_call_response, 'access_token') and hasattr(web_call_response, 'call_id'):
            return {
                "status_code": 200,
                "content": {
                    "access_token": web_call_response.access_token,
                    "call_id": web_call_response.call_id,
                    "agent_id": agent_id
                }
            }
        else:
            return {
                "status_code": 200,
                "content": web_call_response
            }
    except Exception as e:
        logging.error("==== 创建 web call 失败: %s", e)
        return {
            "status_code": 500,
            "content": {
                "message": f"Failed to create web call: {str(e)}"
            }
        }
```

#### 3.2 更新 LLM Prompt (retell_api/llm.py)

```python
def update_llm_begin_message_and_prompt(
    llm_id: str,
    begin_message: str,
    general_prompt: str
) -> str:
    """
    更新 LLM 的开场白和系统 prompt
    
    这允许每次通话都使用个性化的对话内容，例如：
    - "Hi Julia, this is Nina from your clinic..."
    - "I see you have an appointment on Monday..."
    
    Args:
        llm_id: Retell LLM ID
        begin_message: 开场白（AI 第一句话）
        general_prompt: 系统 prompt（AI 行为指令）
    
    Returns:
        llm_id: 更新后的 LLM ID
    """
    retell = get_retell_client()
    try:
        llm_response = retell.llm.update(
            llm_id=llm_id,
            begin_message=begin_message,
            general_prompt=general_prompt,
            start_speaker='agent'
        )
        return llm_response.llm_id
    except Exception as e:
        logging.error("Error updating LLM: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
```

#### 3.3 Retell Client 初始化 (retell_api/client.py)

```python
def get_retell_client() -> Retell:
    """
    初始化 Retell 客户端
    
    环境变量要求：
        RETELL_API_KEY: Retell API 密钥
    
    Returns:
        Retell: Retell 客户端实例
    """
    api_key = os.environ["RETELL_API_KEY"]
    return Retell(api_key=api_key)
```

---

## 🔄 完整调用流程

### 时序图

```
前端应用          FastAPI Backend       Retell API      Retell Platform
    │                    │                   │                 │
    │  1. 用户点击"开始通话"│                   │                 │
    ├──────────────────>│                   │                 │
    │                    │                   │                 │
    │  POST /intake/create-web-call         │                 │
    │  {patient_id: "123"}                  │                 │
    │                    │                   │                 │
    │                    │  2. 获取患者信息   │                 │
    │                    ├──────────────────┐│                 │
    │                    │  (PatientClient) ││                 │
    │                    │<─────────────────┘│                 │
    │                    │                   │                 │
    │                    │  3. 获取预约信息   │                 │
    │                    ├──────────────────┐│                 │
    │                    │ (ClinicEventClient)                 │
    │                    │<─────────────────┘│                 │
    │                    │                   │                 │
    │                    │  4. 更新 LLM Prompt│                 │
    │                    ├──────────────────>│  retell.llm.update()
    │                    │                   ├────────────────>│
    │                    │                   │<────────────────┤
    │                    │<──────────────────┤  Success        │
    │                    │                   │                 │
    │                    │  5. 创建 Web Call  │                 │
    │                    ├──────────────────>│ retell.call.create_web_call()
    │                    │                   ├────────────────>│
    │                    │                   │<────────────────┤
    │                    │<──────────────────┤ {access_token,  │
    │                    │                   │  call_id}       │
    │                    │                   │                 │
    │  6. 返回凭证        │                   │                 │
    │<───────────────────┤                   │                 │
    │  {access_token,    │                   │                 │
    │   call_id,         │                   │                 │
    │   agent_id}        │                   │                 │
    │                    │                   │                 │
    │  7. 初始化 Retell SDK│                  │                 │
    ├──────────────────────────────────────>│                 │
    │  new RetellWebClient()                 │                 │
    │  startCall(access_token)               │                 │
    │                    │                   ├────────────────>│
    │                    │                   │  建立 WebRTC    │
    │<───────────────────────────────────────┼────────────────>│
    │                    │                   │  音频流         │
    │                    │                   │                 │
    │  8. 通话进行中...   │                   │                 │
    │<═══════════════════════════════════════┼────────────────>│
    │                    │                   │                 │
    │  9. 通话结束        │                   │                 │
    ├──────────────────>│                   │                 │
    │  stopCall()        │                   │                 │
    │                    │                   │                 │
    │                    │  10. Webhook 回调 │                 │
    │                    │<──────────────────┼────────────────┤
    │                    │  POST /intake/webhook              │
    │                    │  event: call_ended                 │
    │                    │                   │                 │
    │                    │  11. 保存通话数据 │                 │
    │                    ├──────────────────┐│                 │
    │                    │  (save_call_from_retell_api())     │
    │                    │<─────────────────┘│                 │
    │                    │                   │                 │
    │                    │  12. 生成分析报告 │                 │
    │                    ├──────────────────┐│                 │
    │                    │  (generate_all_analyses_async())   │
    │                    │<─────────────────┘│                 │
```

---

## 📊 数据流设计

### 1. 患者信息获取

```python
# 从 UC (Unified Care) API 获取患者信息
patient_client = PatientClient()
patient_info = patient_client.get_patient_info(patient_id)

# 返回的 PatientInfo 对象包含：
{
    "patient_id": "123456789",
    "patient_name": "Julia Liu",
    "phone_number": "+15108717330",
    "timezone": "US/Pacific",
    "dob": "1990-01-01",
    "doctor_name": "Dr. Smith",
    "business_name": "Health Clinic",
    "address": "123 Main St",
    "clinic_id": "clinic_001"
}
```

### 2. 预约信息获取

```python
# 获取即将到来的预约
clinic_event_client = ClinicEventClient()
response = await clinic_event_client.get_patient_appoint_by_patient_id(patient_id)

# 处理后返回：
upcoming_visit_info = """
**Upcoming Appointment:**
- Date: Monday, November 11, 2025
- Time: 02:00 PM
- With: Dr. Emily Chen (RD)
- Type: Follow Up Visit
- Method: Video Call
"""
dietitian_name = "Dr. Emily Chen"
```

### 3. 动态变量注入

```python
dynamic_variables = {
    "patient_id": "123456789",
    "patient_first_name": "Julia",
    "patient_last_name": "Liu",
    "patient_name": "Julia Liu",
    "patient_dob": "1990-01-01",
    "patient_timezone": "US/Pacific",
    "doctor_name": "Dr. Smith",
    "assigned_rd_name": "Dr. Emily Chen",
    "dietician_name": "Dr. Emily Chen",
    "clinic_name": "Health Clinic",
    "current_date_time": "2025-11-10 14:30:00",
    "timezone": "US/Pacific",
    "upcoming_visit_info": "...",
    "previous_conversation": ""  # 用于恢复中断的通话
}
```

### 4. Prompt 模板填充

```python
# 模板示例（intake_begin_message_template.txt）
begin_message_template = """
Hi {patient_first_name}, this is {dietician_name} from {clinic_name}. 
I'm calling to gather some information before your upcoming appointment. 
Do you have a few minutes to chat?
"""

# 填充后
begin_message = """
Hi Julia, this is Dr. Emily Chen from Health Clinic. 
I'm calling to gather some information before your upcoming appointment. 
Do you have a few minutes to chat?
"""
```

---

## 🌐 前端集成指南

### 1. 安装 Retell Web SDK

```bash
npm install @retell-ai/retell-client-js-sdk
# 或
yarn add @retell-ai/retell-client-js-sdk
```

### 2. React 集成示例

```javascript
import { useEffect, useRef, useState } from 'react';
import { RetellWebClient } from '@retell-ai/retell-client-js-sdk';

function IntakeCallComponent() {
  const retellWebClientRef = useRef(null);
  const [isCallActive, setIsCallActive] = useState(false);
  const [callStatus, setCallStatus] = useState('idle');

  // 初始化 Retell Web Client
  useEffect(() => {
    retellWebClientRef.current = new RetellWebClient();
    
    // 注册事件监听器
    retellWebClientRef.current.on('call_started', () => {
      console.log('Call started');
      setCallStatus('active');
    });

    retellWebClientRef.current.on('call_ended', () => {
      console.log('Call ended');
      setIsCallActive(false);
      setCallStatus('ended');
    });

    retellWebClientRef.current.on('agent_start_talking', () => {
      console.log('Agent started talking');
    });

    retellWebClientRef.current.on('agent_stop_talking', () => {
      console.log('Agent stopped talking');
    });

    retellWebClientRef.current.on('error', (error) => {
      console.error('Retell error:', error);
      setCallStatus('error');
    });

    return () => {
      // 清理
      if (retellWebClientRef.current) {
        retellWebClientRef.current.stopCall();
      }
    };
  }, []);

  // 开始通话
  const startCall = async () => {
    try {
      // 步骤 1: 调用后端 API 创建 web call
      const response = await fetch('http://localhost:8000/intake/create-web-call', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: '123456789',  // 可选
          // previous_transcript: []  // 可选，用于恢复通话
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create web call');
      }

      const data = await response.json();
      console.log('Web call created:', data);

      // 步骤 2: 使用返回的 access_token 启动通话
      await retellWebClientRef.current.startCall({
        accessToken: data.access_token,
        sampleRate: 24000,  // 可选: 24000 或 16000
        enableUpdate: true,  // 可选: 启用实时更新
      });

      setIsCallActive(true);
      setCallStatus('connecting');

    } catch (error) {
      console.error('Error starting call:', error);
      setCallStatus('error');
    }
  };

  // 结束通话
  const stopCall = async () => {
    if (retellWebClientRef.current) {
      retellWebClientRef.current.stopCall();
      setIsCallActive(false);
    }
  };

  return (
    <div className="intake-call-container">
      <h2>Intake Call</h2>
      <p>Status: {callStatus}</p>
      
      {!isCallActive ? (
        <button onClick={startCall} disabled={callStatus === 'connecting'}>
          {callStatus === 'connecting' ? 'Connecting...' : 'Start Call'}
        </button>
      ) : (
        <button onClick={stopCall}>
          End Call
        </button>
      )}
    </div>
  );
}

export default IntakeCallComponent;
```

### 3. Vue.js 集成示例

```vue
<template>
  <div class="intake-call-container">
    <h2>Intake Call</h2>
    <p>Status: {{ callStatus }}</p>
    
    <button 
      v-if="!isCallActive" 
      @click="startCall" 
      :disabled="callStatus === 'connecting'"
    >
      {{ callStatus === 'connecting' ? 'Connecting...' : 'Start Call' }}
    </button>
    
    <button 
      v-else 
      @click="stopCall"
    >
      End Call
    </button>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { RetellWebClient } from '@retell-ai/retell-client-js-sdk';

export default {
  name: 'IntakeCallComponent',
  setup() {
    const retellWebClient = ref(null);
    const isCallActive = ref(false);
    const callStatus = ref('idle');

    onMounted(() => {
      // 初始化 Retell Web Client
      retellWebClient.value = new RetellWebClient();

      // 注册事件监听器
      retellWebClient.value.on('call_started', () => {
        console.log('Call started');
        callStatus.value = 'active';
      });

      retellWebClient.value.on('call_ended', () => {
        console.log('Call ended');
        isCallActive.value = false;
        callStatus.value = 'ended';
      });

      retellWebClient.value.on('error', (error) => {
        console.error('Retell error:', error);
        callStatus.value = 'error';
      });
    });

    onUnmounted(() => {
      // 清理
      if (retellWebClient.value) {
        retellWebClient.value.stopCall();
      }
    });

    const startCall = async () => {
      try {
        // 调用后端 API 创建 web call
        const response = await fetch('http://localhost:8000/intake/create-web-call', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            patient_id: '123456789',
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to create web call');
        }

        const data = await response.json();
        console.log('Web call created:', data);

        // 使用 access_token 启动通话
        await retellWebClient.value.startCall({
          accessToken: data.access_token,
          sampleRate: 24000,
          enableUpdate: true,
        });

        isCallActive.value = true;
        callStatus.value = 'connecting';

      } catch (error) {
        console.error('Error starting call:', error);
        callStatus.value = 'error';
      }
    };

    const stopCall = () => {
      if (retellWebClient.value) {
        retellWebClient.value.stopCall();
        isCallActive.value = false;
      }
    };

    return {
      isCallActive,
      callStatus,
      startCall,
      stopCall,
    };
  },
};
</script>

<style scoped>
.intake-call-container {
  padding: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 4. 恢复中断的通话

如果通话意外中断，可以使用 `previous_transcript` 参数恢复对话：

```javascript
// 假设你保存了之前的对话记录
const previousTranscript = [
  { role: 'agent', content: 'Hello Julia, how are you today?' },
  { role: 'user', content: 'I\'m doing well, thank you.' },
  { role: 'agent', content: 'Great! Let me ask about your diet...' },
];

// 创建 web call 时传递历史记录
const response = await fetch('http://localhost:8000/intake/create-web-call', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    patient_id: '123456789',
    previous_transcript: previousTranscript,  // 传递历史对话
  }),
});
```

AI 会在 prompt 中接收到历史对话，从而可以继续之前的话题。

---

## 🔐 安全性考虑

### 1. API 密钥管理

```python
# ❌ 错误：硬编码 API 密钥
RETELL_API_KEY = "key_abc123xyz456"

# ✅ 正确：使用环境变量
import os
RETELL_API_KEY = os.environ["RETELL_API_KEY"]
```

**环境变量配置**:
```bash
# .env 文件
RETELL_API_KEY=key_e3b74c0de01a1ba9c20228131da1
OPENAI_API_KEY=sk-proj-...
```

### 2. Webhook 签名验证

Retell 会在 webhook 请求中包含签名，用于验证请求来源：

```python
from utils.auth import verify_retell_signature

@intake_router.post("/webhook")
async def intake_webhook(request: Request):
    """处理 Retell webhook 回调"""
    post_data = await request.json()
    
    # 验证签名
    api_key = os.environ["RETELL_API_KEY"]
    if not verify_retell_signature(dict(request.headers), post_data, api_key):
        logging.warning("==== Unauthorized webhook request")
        return JSONResponse(status_code=401, content={"status": "unauthorized"})
    
    # 处理 webhook 事件
    # ...
```

### 3. CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 开发环境
        "https://yourdomain.com",  # 生产环境
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 📞 Webhook 事件处理

### Webhook 端点

**端点**: `POST /intake/webhook`

**功能**: 接收 Retell 平台发送的通话事件通知。

### 事件类型

Retell 会发送以下事件：

1. **call_started**: 通话开始
2. **call_ended**: 通话结束
3. **call_analyzed**: 通话分析完成（包含 transcript 和其他数据）

### Webhook Handler 实现

```python
async def handle_intake_webhook(
    request: Request,
    db: Optional[Any] = None,
    post_data: Dict[str, Any] = None
) -> JSONResponse:
    """
    处理 Retell webhook 事件
    
    主要流程：
    1. call_started: 记录通话开始（可选）
    2. call_ended: 
       - 从 Retell API 获取完整通话数据
       - 保存到 CSV 文件
       - 触发后台分析生成（summary, evaluation, goal analysis）
    3. call_analyzed: 数据已在 call_ended 时保存，无需额外操作
    """
    call = post_data.get("call", {})
    call_id = call.get("call_id", "Unknown")
    event_type = post_data.get("event")
    
    logging.info(f"==== Webhook event: {event_type}, call_id: {call_id}")
    
    match event_type:
        case "call_started":
            logging.info(f"==== Call started: {call_id}")
        
        case "call_ended":
            try:
                # 从 Retell API 获取完整通话数据并保存
                logging.info(f"==== Fetching call data from Retell API: {call_id}")
                save_call_from_retell_api(call_id)
                logging.info(f"==== ✅ Saved call data to CSV: {call_id}")
                
                # 后台生成分析报告（非阻塞）
                async def generate_and_save():
                    try:
                        from .retell_data_storage import get_call_data_from_csv
                        from .llm_generation_service import generate_all_analyses_async, save_analyses_to_csv
                        
                        # 获取患者信息
                        call_data = get_call_data_from_csv(call_id)
                        patient_id = call_data.get("patient_id", "")
                        patient_name = call_data.get("patient_name", "the patient")
                        
                        # 生成所有分析（summary, goal, evaluation）
                        analyses = await generate_all_analyses_async(
                            call_id=call_id,
                            transcript_object=None,  # 从 Retell/CSV 获取
                            patient_id=patient_id,
                            patient_name=patient_name
                        )
                        
                        # 保存到 CSV
                        if analyses:
                            save_analyses_to_csv(call_id, analyses)
                            logging.info(f"==== ✅ Saved analyses to CSV: {call_id}")
                        
                    except Exception as e:
                        logging.error(f"==== ❌ Failed to generate analyses: {e}", exc_info=True)
                
                # 创建后台任务
                asyncio.create_task(generate_and_save())
                
            except Exception as e:
                logging.error(f"==== ❌ Failed to save call data: {e}", exc_info=True)
        
        case "call_analyzed":
            logging.info(f"==== Call analyzed: {call_id}")
        
        case _:
            logging.warning(f"==== Unknown event type: {event_type}")
    
    return JSONResponse(status_code=200, content={"status": "success"})
```

### Retell 平台 Webhook 配置

在 Retell 平台的 Agent 配置页面设置 webhook URL：

```
https://yourdomain.com/intake/webhook
```

**注意**：
- Webhook URL 必须是公网可访问的 HTTPS 地址
- 本地开发可以使用 ngrok 等工具暴露本地服务：
  ```bash
  ngrok http 8000
  # 使用 ngrok 提供的 URL: https://abc123.ngrok.io/intake/webhook
  ```

---

## 💾 数据存储设计

### CSV 文件结构

通话数据保存在 `intake_phone_agent/results/intake_calls_full_data.csv`：

```csv
call_id,patient_id,patient_name,agent_id,call_type,call_status,start_timestamp,end_timestamp,duration_seconds,transcript,transcript_object,recording_url,call_summary,llm_generated_summary,llm_goal_analysis,data_completeness_evaluation,safety_empathy_time_evaluation,created_at
call_abc123,123456789,Julia Liu,agent_e058...,intake_web_call,ended,2025-11-10T14:30:00Z,2025-11-10T14:45:00Z,900,"...","{...}",https://...,"{...}","{...}","{...}","{...}","{...}",2025-11-10T14:45:30Z
```

**主要字段**：
- `call_id`: Retell 通话 ID（唯一标识）
- `patient_id`: 患者 ID
- `patient_name`: 患者姓名
- `agent_id`: Retell Agent ID
- `call_type`: 通话类型（intake_web_call / intake_phone_call）
- `call_status`: 通话状态（registered, ongoing, ended, error）
- `transcript`: 对话文本（纯文本格式）
- `transcript_object`: 对话记录（JSON 格式，包含 role 和 content）
- `recording_url`: 录音文件 URL
- `llm_generated_summary`: LLM 生成的结构化摘要（JSON）
- `llm_goal_analysis`: 目标达成分析（JSON）
- `data_completeness_evaluation`: 数据完整性评估（JSON）
- `safety_empathy_time_evaluation`: 安全性/共情/时间评估（JSON）

### 数据保存流程

```python
from .retell_data_storage import save_call_from_retell_api

def save_call_from_retell_api(call_id: str):
    """
    从 Retell API 获取完整通话数据并保存到 CSV
    
    步骤：
    1. 调用 Retell API 获取通话详情
    2. 提取所有相关字段
    3. 保存/更新 CSV 文件中的记录
    """
    try:
        # 获取 Retell client
        retell = get_retell_client()
        
        # 调用 API 获取通话数据
        call_data = retell.call.retrieve(call_id)
        
        # 提取字段
        call_dict = {
            "call_id": call_data.call_id,
            "agent_id": call_data.agent_id,
            "call_type": call_data.metadata.get("call_type", ""),
            "call_status": call_data.call_status,
            "start_timestamp": call_data.start_timestamp,
            "end_timestamp": call_data.end_timestamp,
            "duration_seconds": call_data.end_timestamp - call_data.start_timestamp,
            "transcript": call_data.transcript,
            "transcript_object": json.dumps(call_data.transcript_object),
            "recording_url": call_data.recording_url,
            "patient_id": call_data.metadata.get("patient_id", ""),
            "patient_name": call_data.metadata.get("patient_name", ""),
            # ... 其他字段
        }
        
        # 保存到 CSV
        _save_to_csv(call_dict)
        
    except Exception as e:
        logging.error(f"Failed to save call data: {e}", exc_info=True)
```

---

## 🧪 测试指南

### 1. 后端 API 测试

#### 使用 curl

```bash
# 测试创建 web call
curl -X POST http://localhost:8000/intake/create-web-call \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "123456789"
  }'

# 预期响应
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "call_id": "call_abc123xyz456",
  "agent_id": "agent_e0582ed7942755487668942253",
  "patient_name": "Julia Liu",
  "message": "Web call created successfully"
}
```

#### 使用 Postman

1. 创建新请求：`POST http://localhost:8000/intake/create-web-call`
2. Headers: `Content-Type: application/json`
3. Body (raw JSON):
```json
{
  "patient_id": "123456789"
}
```
4. 发送请求，检查响应

### 2. 前端集成测试

#### 测试 Retell SDK 初始化

```javascript
// 在浏览器控制台测试
import { RetellWebClient } from '@retell-ai/retell-client-js-sdk';

const client = new RetellWebClient();
console.log('Retell client initialized:', client);

// 测试事件监听
client.on('call_started', () => {
  console.log('✅ Call started event fired');
});

client.on('error', (error) => {
  console.error('❌ Retell error:', error);
});
```

#### 完整端到端测试

```javascript
async function testWebCall() {
  try {
    // 1. 创建 web call
    console.log('Step 1: Creating web call...');
    const response = await fetch('http://localhost:8000/intake/create-web-call', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_id: '123456789' }),
    });
    
    const data = await response.json();
    console.log('✅ Web call created:', data);
    
    // 2. 初始化 Retell client
    console.log('Step 2: Initializing Retell client...');
    const retellClient = new RetellWebClient();
    
    // 3. 启动通话
    console.log('Step 3: Starting call with access token...');
    await retellClient.startCall({
      accessToken: data.access_token,
      sampleRate: 24000,
    });
    
    console.log('✅ Call started successfully');
    
    // 4. 等待 10 秒后结束通话（用于测试）
    setTimeout(() => {
      console.log('Step 4: Stopping call...');
      retellClient.stopCall();
      console.log('✅ Call stopped');
    }, 10000);
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// 运行测试
testWebCall();
```

### 3. Webhook 测试

#### 模拟 Retell Webhook 请求

```bash
# 模拟 call_ended 事件
curl -X POST http://localhost:8000/intake/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "call_ended",
    "call": {
      "call_id": "call_test123",
      "call_status": "ended",
      "agent_id": "agent_e0582ed7942755487668942253"
    }
  }'
```

**注意**: 生产环境需要验证 Retell 签名，测试时可以临时禁用：

```python
# utils/auth.py - 仅用于测试
def verify_retell_signature(headers, body, api_key):
    # 临时禁用签名验证（生产环境必须启用）
    return True
```

---

## 🚀 部署指南

### 1. 环境变量配置

创建 `.env` 文件：

```bash
# Retell API
RETELL_API_KEY=key_e3b74c0de01a1ba9c20228131da1
RETELL_PHONE_NUMBER=+18668991727  # 可选，用于 phone call

# OpenAI API（用于生成 summary 和 evaluation）
OPENAI_API_KEY=sk-proj-...

# 数据库（可选，测试时可不配置）
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# 其他配置
ENVIRONMENT=prod  # dev / prod
SESSION_SECRET_KEY=your-secret-key-here
```

### 2. 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# 主要依赖包括：
# - fastapi
# - uvicorn
# - retell-sdk
# - openai
# - python-dotenv
# - httpx
# - pandas  # 用于 CSV 操作
```

### 3. 启动服务

```bash
# 开发环境
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 使用 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 构建镜像
docker build -t intake-phone-agent .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -e RETELL_API_KEY=key_xxx \
  -e OPENAI_API_KEY=sk-proj-xxx \
  --name intake-agent \
  intake-phone-agent
```

### 5. Nginx 反向代理配置

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /intake/ {
        proxy_pass http://localhost:8000/intake/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket 支持（Retell 可能需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 📚 最佳实践

### 1. 错误处理

```python
async def create_intake_web_call(...):
    try:
        # 主逻辑
        patient_info = patient_client.get_patient_info(patient_id)
        
    except HTTPException as e:
        # FastAPI 异常，直接抛出
        raise e
        
    except Exception as e:
        # 其他异常，记录日志并返回友好错误
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return {
            "status_code": 500,
            "content": {
                "message": "Internal server error",
                "error": str(e)
            }
        }
```

### 2. 日志记录

```python
import logging

# 使用结构化日志
logging.info(f"==== Creating web call for patient_id: {patient_id}")
logging.info(f"==== Patient info: name={patient_name}, timezone={timezone}")
logging.info(f"==== Web call created: call_id={call_id}, access_token=***")

# 错误日志包含堆栈信息
try:
    # ...
except Exception as e:
    logging.error(f"==== Failed to create web call: {e}", exc_info=True)
```

### 3. 降级策略

```python
# 获取患者信息失败时使用默认数据
try:
    patient_info = patient_client.get_patient_info(patient_id)
except Exception as e:
    logging.error(f"Failed to fetch patient info: {e}")
    # 使用默认数据，确保服务可用
    patient_info = PatientInfo(
        patient_id=patient_id,
        patient_name=f"Patient {patient_id[:8]}",
        timezone="US/Pacific"
    )
```

### 4. 幂等性设计

```python
# Webhook 可能会重复发送，确保幂等性
def save_call_from_retell_api(call_id: str):
    """保存通话数据（幂等操作）"""
    # 检查记录是否已存在
    existing = get_call_data_from_csv(call_id)
    if existing:
        logging.info(f"Call data already exists: {call_id}, updating...")
        # 更新而不是插入
    else:
        logging.info(f"Saving new call data: {call_id}")
    
    # 保存/更新数据
    _save_to_csv(call_dict)
```

### 5. 性能优化

```python
# 使用异步操作避免阻塞
async def create_intake_web_call(...):
    # 并发获取患者信息和预约信息
    patient_info_task = asyncio.create_task(get_patient_info(patient_id))
    visit_info_task = asyncio.create_task(get_upcoming_visit_info(patient_id))
    
    patient_info = await patient_info_task
    visit_info = await visit_info_task
    
    # 继续处理...
```

```python
# 后台任务处理耗时操作
async def handle_webhook(...):
    # 保存基础数据（快速）
    save_call_from_retell_api(call_id)
    
    # 生成分析报告（慢）- 放到后台
    asyncio.create_task(generate_all_analyses_async(call_id))
    
    # 立即返回响应给 Retell
    return JSONResponse(status_code=200, content={"status": "success"})
```

---

## ⚠️ 常见问题

### 1. access_token 过期

**问题**: 前端报错 "Invalid or expired access token"

**原因**: access_token 有时效限制（通常 24 小时）

**解决方案**:
```javascript
// 检测 token 过期并重新创建
retellClient.on('error', async (error) => {
  if (error.message.includes('expired')) {
    console.log('Access token expired, creating new call...');
    await createNewWebCall();
  }
});
```

### 2. Microphone 权限被拒绝

**问题**: 浏览器无法获取麦克风权限

**解决方案**:
- 确保网站使用 HTTPS（localhost 除外）
- 在启动通话前请求权限：
```javascript
async function requestMicrophonePermission() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(track => track.stop());
    return true;
  } catch (error) {
    console.error('Microphone permission denied:', error);
    return false;
  }
}

// 在 startCall 前调用
const hasPermission = await requestMicrophonePermission();
if (hasPermission) {
  await startCall();
}
```

### 3. Webhook 未收到

**问题**: 通话结束后，webhook 未被触发

**可能原因**:
1. Webhook URL 配置错误
2. 服务不可公网访问
3. 防火墙阻止

**排查步骤**:
```bash
# 1. 检查 Retell 平台的 webhook 配置
# 2. 测试 URL 是否可公网访问
curl https://yourdomain.com/intake/webhook

# 3. 本地开发使用 ngrok
ngrok http 8000
# 将 ngrok URL 配置到 Retell: https://abc123.ngrok.io/intake/webhook

# 4. 查看服务器日志
tail -f logs/app.log | grep webhook
```

### 4. 音频质量差

**问题**: 通话音质不佳，有延迟或卡顿

**解决方案**:
```javascript
// 调整采样率
await retellClient.startCall({
  accessToken: token,
  sampleRate: 16000,  // 尝试降低采样率（默认 24000）
  enableUpdate: false,  // 禁用实时更新减少负载
});
```

### 5. 中文识别问题

**问题**: AI 无法正确识别中文语音

**解决方案**: Retell 目前主要支持英文，中文支持有限。如需中文语音识别，建议：
- 使用专门的中文语音识别服务（如阿里云、腾讯云）
- 或切换到支持中文的 AI 平台

---

## 📖 相关文档

### 项目内部文档
- `QUICK_START.md`: 快速开始指南
- `RETELL_DATA_STORAGE_GUIDE.md`: 数据存储详细说明
- `TESTING_GUIDE.md`: 测试指南
- `README.md`: 项目概览

### 外部资源
- [Retell AI 官方文档](https://docs.retell.ai/)
- [Retell Web SDK 文档](https://docs.retell.ai/sdk-reference/web-sdk)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [OpenAI API 文档](https://platform.openai.com/docs/)

---

## 🔄 更新日志

### v1.0 (2025-11-10)
- ✅ 初始版本
- ✅ 完整的 web call 创建流程
- ✅ 患者信息动态注入
- ✅ Webhook 事件处理
- ✅ LLM 分析生成（summary, evaluation, goal analysis）
- ✅ CSV 数据存储
- ✅ 前端集成示例（React/Vue）

---

## 👥 技术支持

如有问题，请联系：

- **开发团队**: Minerva Development Team
- **邮箱**: dev@minerva.com（示例）
- **项目仓库**: [内部 GitLab/GitHub 链接]

---

## 📄 许可证

[根据项目实际情况填写]

---

**文档结束**

