'use client';

import { useState, useEffect } from 'react';
import styles from './security.module.css';

export default function SecurityPage() {
  const [passwordData, setPasswordData] = useState({ current: '', new: '', confirm: '' });
  const [is2FAEnabled, setIs2FAEnabled] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const mockActivity = [
    { id: 1, event: 'Login', device: 'Chrome / Windows', location: 'Mumbai, IN', time: 'Just now', status: 'success' },
    { id: 2, event: 'Transfer', device: 'Edge / Windows', location: 'Delhi, IN', time: '2h ago', status: 'success' },
    { id: 3, event: 'Login', device: 'Safari / iPhone', location: 'Pune, IN', time: 'Yesterday', status: 'failed' },
    { id: 4, event: 'Settings Change', device: 'Chrome / Windows', location: 'Mumbai, IN', time: '2 days ago', status: 'success' }
  ];

  const handlePasswordChange = (e) => {
    e.preventDefault();
    if (passwordData.new !== passwordData.confirm) {
      setMessage({ type: 'error', text: 'Passwords do not match!' });
      return;
    }
    // Mock success
    setMessage({ type: 'success', text: 'Password updated successfully!' });
    setPasswordData({ current: '', new: '', confirm: '' });
    setTimeout(() => setMessage({ type: '', text: '' }), 3000);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Security Center</h1>
          <p className={styles.subtitle}>Manage your account protection and monitoring</p>
        </div>
      </header>

      <div className={styles.grid}>
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Change Password</h3>
          <form className={styles.form} onSubmit={handlePasswordChange}>
            <div className={styles.inputGroup}>
              <label>Current Password</label>
              <input 
                type="password" 
                value={passwordData.current}
                onChange={(e) => setPasswordData({...passwordData, current: e.target.value})}
                placeholder="••••••••" 
                required 
              />
            </div>
            <div className={styles.inputGroup}>
              <label>New Password</label>
              <input 
                type="password" 
                value={passwordData.new}
                onChange={(e) => setPasswordData({...passwordData, new: e.target.value})}
                placeholder="••••••••" 
                required 
              />
            </div>
            <div className={styles.inputGroup}>
              <label>Confirm New Password</label>
              <input 
                type="password" 
                value={passwordData.confirm}
                onChange={(e) => setPasswordData({...passwordData, confirm: e.target.value})}
                placeholder="••••••••" 
                required 
              />
            </div>
            {message.text && (
              <div className={`${styles.message} ${styles[message.type]}`}>
                {message.text}
              </div>
            )}
            <button type="submit" className={styles.submitBtn}>Update Password</button>
          </form>

          <div className={styles.twoFactor}>
            <div className={styles.tfaInfo}>
              <h4 className={styles.tfaTitle}>Two-Factor Authentication (2FA)</h4>
              <p className={styles.tfaDesc}>Add an extra layer of security to your account.</p>
            </div>
            <label className={styles.switch}>
              <input type="checkbox" checked={is2FAEnabled} onChange={() => setIs2FAEnabled(!is2FAEnabled)} />
              <span className={styles.slider}></span>
            </label>
          </div>
        </div>

        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Recent Security Activity</h3>
          <div className={styles.activityList}>
            {mockActivity.map(act => (
              <div key={act.id} className={styles.activityItem}>
                <div className={`${styles.statusDot} ${styles[act.status]}`}></div>
                <div className={styles.activityContent}>
                  <div className={styles.activityHeader}>
                    <span className={styles.event}>{act.event}</span>
                    <span className={styles.time}>{act.time}</span>
                  </div>
                  <div className={styles.activityMeta}>
                    <span>{act.device}</span>
                    <span>•</span>
                    <span>{act.location}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button className={styles.viewAllBtn}>View All Activity</button>
        </div>
      </div>
    </div>
  );
}
