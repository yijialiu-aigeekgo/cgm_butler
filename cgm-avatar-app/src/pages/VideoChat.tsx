import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

export function VideoChat() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#F8F9FA] flex flex-col max-w-[430px] mx-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center flex-shrink-0">
        <button onClick={() => navigate('/')} className="p-2 -ml-2 active:bg-gray-100 rounded-full">
          <ArrowLeft className="w-6 h-6 text-gray-700" />
        </button>
        <h1 className="text-gray-800 ml-3">Video Chat</h1>
      </div>

      {/* Content */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center">
          <h2 className="text-gray-700 mb-4 text-xl">Video Chat</h2>
          <p className="text-gray-500 mb-6">Coming soon...</p>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-[#5B7FF3] text-white rounded-full hover:bg-[#4A6FE2] transition-colors"
          >
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
