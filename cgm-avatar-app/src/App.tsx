import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UserProvider } from './contexts/UserContext';
import { OliviaHome } from './pages/OliviaHome';
import { VoiceChat } from './pages/VoiceChat';
import { VideoChat } from './pages/VideoChat';

export default function App() {
  return (
    <UserProvider>
      <Router>
        <div className="min-h-screen bg-[#F8F9FA]">
          <Routes>
            <Route path="/" element={<OliviaHome />} />
            <Route path="/voice-chat" element={<VoiceChat />} />
            <Route path="/video-chat" element={<VideoChat />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}
