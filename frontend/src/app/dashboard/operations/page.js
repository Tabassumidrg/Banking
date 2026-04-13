'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from './operations.module.css';

export default function OperationsPage() {
  const [activeTab, setActiveTab] = useState('kyc');
  const [pendingKYC, setPendingKYC] = useState([]);
  const [serviceRequests, setServiceRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://banking-backend-api.onrender.com';
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const u = JSON.parse(storedUser);
      if (u.role !== 'admin' && u.email !== 'nidhi.sharma@nidhi.bank') {
        router.push('/dashboard');
        return;
      }
    } else {
      router.push('/login');
      return;
    }
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'kyc') {
        const res = await fetch(`${backendUrl}/api/admin/kyc/pending`);
        if (res.ok) {
          const data = await res.json();
          setPendingKYC(data);
        }
      } else {
        const res = await fetch(`${backendUrl}/api/admin/service-requests`);
        if (res.ok) {
          const data = await res.json();
          setServiceRequests(data);
        }
      }
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateKYC = async (userId, status) => {
    const notes = window.prompt(`Optional notes for ${status}:`) || "";
    try {
      const res = await fetch(`${backendUrl}/api/admin/kyc/update`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, status, notes })
      });
      if (res.ok) {
        alert(`User KYC ${status} successfully!`);
        fetchData();
      }
    } catch (err) {
      alert("Update failed");
    }
  };

  const handleUpdateServiceStatus = async (requestId, status) => {
    try {
      const res = await fetch(`${backendUrl}/api/admin/service-requests/${requestId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });
      if (res.ok) {
        setServiceRequests(prev => prev.map(r => r.id === requestId ? { ...r, status } : r));
      }
    } catch (err) {
      alert("Update failed");
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>Branch Operations Hub</h1>
          <p className={styles.subtitle}>Manage compliance and customer service fulfillment</p>
        </div>
      </header>

      <div className={styles.tabs}>
        <button 
          className={`${styles.tab} ${activeTab === 'kyc' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('kyc')}
        >
          KYC Queue {pendingKYC.length > 0 && `(${pendingKYC.length})`}
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'requests' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('requests')}
        >
          Service Requests
        </button>
      </div>

      <div className={styles.content}>
        {loading ? (
          <div className={styles.empty}>Loading operations data...</div>
        ) : activeTab === 'kyc' ? (
          pendingKYC.length > 0 ? (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th className={styles.th}>Member</th>
                  <th className={`${styles.th} ${styles.hideMobile}`}>Email</th>
                  <th className={styles.th}>Joined</th>
                  <th className={styles.th}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {pendingKYC.map(u => (
                  <tr key={u.id} className={styles.tr}>
                    <td className={styles.td}>
                      <strong>{u.full_name}</strong>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>ID: #NB-{u.id}</div>
                    </td>
                    <td className={`${styles.td} ${styles.hideMobile}`}>{u.email}</td>
                    <td className={styles.td}>{new Date(u.created_at).toLocaleDateString()}</td>
                    <td className={styles.td}>
                      <div className={styles.actions}>
                        <button className={`${styles.actionBtn} ${styles.verifyBtn}`} onClick={() => handleUpdateKYC(u.id, 'verified')}>Approve</button>
                        <button className={`${styles.actionBtn} ${styles.rejectBtn}`} onClick={() => handleUpdateKYC(u.id, 'rejected')}>Reject</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className={styles.empty}>Zero pending KYC verifications. All users compliant.</div>
          )
        ) : (
          serviceRequests.length > 0 ? (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th className={styles.th}>Request Type</th>
                  <th className={styles.th}>Customer</th>
                  <th className={`${styles.th} ${styles.hideMobile}`}>Details</th>
                  <th className={styles.th}>Current Status</th>
                  <th className={styles.th}>Update</th>
                </tr>
              </thead>
              <tbody>
                {serviceRequests.map(r => (
                  <tr key={r.id} className={styles.tr}>
                    <td className={styles.td}>
                      <span style={{ fontWeight: 700 }}>{r.type.toUpperCase()}</span>
                      <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Req #{r.id}</div>
                    </td>
                    <td className={styles.td}>
                      {r.user_name}
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{r.user_email}</div>
                    </td>
                    <td className={`${styles.td} ${styles.hideMobile}`}>{r.details}</td>
                    <td className={styles.td}>
                      <span className={`${styles.badge} ${styles[r.status]}`}>{r.status}</span>
                    </td>
                    <td className={styles.td}>
                      <select 
                        className={styles.statusSelect}
                        value={r.status}
                        onChange={(e) => handleUpdateServiceStatus(r.id, e.target.value)}
                      >
                        <option value="pending">Pending</option>
                        <option value="processing">Processing</option>
                        <option value="dispatched">Dispatched</option>
                        <option value="completed">Completed</option>
                        <option value="rejected">Rejected</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className={styles.empty}>No service requests found in the system.</div>
          )
        )}
      </div>
    </div>
  );
}
