import React, { createContext, useContext, ReactNode } from 'react';

interface UserContextValue {
  userId: string;
  userName: string;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // 演示阶段：使用默认用户 ID
  const defaultUserId = import.meta.env.VITE_DEFAULT_USER_ID || 'user_001';
  
  const value: UserContextValue = {
    userId: defaultUserId,
    userName: 'John Doe', // 可选：从环境变量或 API 获取
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};


