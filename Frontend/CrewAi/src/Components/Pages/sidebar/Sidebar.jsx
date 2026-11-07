import React from 'react'
import "./Sidebar.css"
const Sidebar = () => {
  return (
    <div>
      <aside className="chat-sidebar">
        <div className="sidebar-header">
          <a className="chat-brand" href="/">
            <span className="brand-mark">C</span>
            <span>Crew<span className="brand-accent">Ai</span></span>
          </a>

          <button className="icon-button" aria-label="Toggle sidebar">
            <svg viewBox="0 0 24 24" fill="none">
              <rect x="3.5" y="4" width="17" height="16" rx="3" />
              <path d="M9 4v16" />
            </svg>
          </button>
        </div>

      
        <div className="sidebar-actions">
          <button className="new-chat-button">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 5v14M5 12h14" />
            </svg>
            <span>New chat</span>
          </button>

      
        </div>

        <div className="history-container">
          <p className="sidebar-label">YOUR CHATS</p>
          
          {/* Chat history will be rendered here later. */}
        </div>

        <div className="sidebar-bottom">
          <div className="sidebar-divider" />

          <button className="sidebar-action">
            <svg viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="9" />
              <path d="M12 11v5M12 8h.01" />
            </svg>
            <span>Help & documentation</span>
          </button>

          <button className="profile-card">
            <div className="profile-avatar">U</div>
            <div className="profile-info">
              <span className="profile-name">Your account</span>
              <span className="profile-plan">CrewAi workspace</span>
            </div>
            <svg className="profile-menu" viewBox="0 0 24 24" fill="none">
              <circle cx="5" cy="12" r="1" />
              <circle cx="12" cy="12" r="1" />
              <circle cx="19" cy="12" r="1" />
            </svg>
          </button>
        </div>
      </aside>
    </div>
  )
}

export default Sidebar
