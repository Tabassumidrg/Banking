'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from '../dashboard.module.css';

export default function AuditLogsPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://banking-backend-api.onrender.com';

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) {
      router.push('/login');
      return;
    }
    const user = JSON.parse(storedUser);
    if (user.role !== 'admin' && user.email !== 'nidhi.sharma@nidhi.bank') {
      router.push('/dashboard');
      return;
    }

    const fetchLogs = async () => {
      try {
        const res = await fetch(`${backendUrl}/api/admin/audit-logs`);
        if (res.ok) {
          const data = await res.json();
          setLogs(data);
        }
      } catch (err) {
        console.error("Failed to fetch audit logs", err);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, [router, backendUrl]);

  if (loading) return <div className={styles.loading}>Loading system audit logs...</div>;

  return (
    <div className={styles.container}>
      <header className={styles.header} style={{ marginBottom: '30px' }}>
        <div>
          <h1 className={styles.title}>System Audit Logs</h1>
          <p className={styles.subtitle}>Complete history of administrative actions and security events</p>
        </div>
      </header>

      <div className={styles.logList} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {logs.map((log) => (
          <div key={log.id} style={{ 
            background: 'rgba(255, 255, 255, 0.03)', 
            border: '1px solid rgba(255, 255, 255, 0.05)', 
            padding: '20px', 
            borderRadius: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ 
                fontWeight: '600', 
                color: log.action.includes('FAILED') ? '#f87171' : '#fbbf24',
                fontSize: '13px',
                letterSpacing: '1px',
                textTransform: 'uppercase'
              }}>{log.action}</span>
              <span style={{ fontSize: '12px', color: '#64748b' }}>{new Date(log.created_at).toLocaleString()}</span>
            </div>
            <div style={{ fontSize: '15px', color: '#e2e8f0' }}>{log.details}</div>
            <div style={{ display: 'flex', gap: '20px', fontSize: '12px', color: '#94a3b8' }}>
              <span>User: <strong>{log.user_name || 'System / Admin'}</strong> ({log.user_email || 'n/a'})</span>
              {log.ip_address && <span>IP: {log.ip_address}</span>}
            </div>
          </div>
        ))}
        {logs.length === 0 && <p style={{ textAlign: 'center', color: '#94a3b8' }}>No logs found in the system history.</p>}
      </div>
    </div>
  );
}
