'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from './requests.module.css';

export default function SupportRequestsPage() {
  const [user, setUser] = useState(null);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    type: 'debit_card',
    details: ''
  });

  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://banking-backend-api.onrender.com';
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) {
      router.push('/login');
      return;
    }
    const parsedUser = JSON.parse(storedUser);
    setUser(parsedUser);
    fetchUserRequests(parsedUser.id);
  }, []);

  const fetchUserRequests = async (userId) => {
    try {
      // We don't have a specific user-requests endpoint yet, 
      // but we can fetch all and filter or add one.
      // For now, let's just fetch all and filter client side for MVP
      const res = await fetch(`${backendUrl}/api/admin/service-requests`);
      if (res.ok) {
        const data = await res.json();
        setRequests(data.filter(r => r.user_id === userId));
      }
    } catch (err) {
      console.error("Fetch history failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setSuccess('');

    try {
      const res = await fetch(`${backendUrl}/api/user/service-requests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          type: formData.type,
          details: formData.details
        })
      });

      if (res.ok) {
        setSuccess('Your request has been submitted successfully! Our team will process it shortly.');
        setFormData({ ...formData, details: '' });
        fetchUserRequests(user.id);
      }
    } catch (err) {
      alert("Submission failed. Please try again later.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Service & Support Hub</h1>
        <p className={styles.subtitle}>Request bank services and track their fulfillment status</p>
      </header>

      <div className={styles.card}>
        <form onSubmit={handleSubmit}>
          {success && <div className={styles.successMsg}>{success}</div>}
          
          <div className={styles.formGroup}>
            <label>Request Type</label>
            <select 
              className={styles.select}
              value={formData.type}
              onChange={(e) => setFormData({...formData, type: e.target.value})}
              required
            >
              <option value="debit_card">New Debit Card Issuance</option>
              <option value="cheque_book">Cheque Book Request</option>
              <option value="account_upgrade">Premium Account Upgrade</option>
              <option value="address_change">Address Change Request</option>
              <option value="other">Other Inquiry / Support</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label>Additional Details</label>
            <textarea 
              className={styles.textarea}
              placeholder="Please provide any specific details or preferences..."
              value={formData.details}
              onChange={(e) => setFormData({...formData, details: e.target.value})}
              required
            />
          </div>

          <button 
            type="submit" 
            className={styles.submitBtn}
            disabled={submitting}
          >
            {submitting ? 'Submitting Request...' : 'Submit Service Request'}
          </button>
        </form>
      </div>

      <div className={styles.historySection}>
        <h2 className={styles.historyTitle}>Your Recent Requests</h2>
        {loading ? (
          <p>Loading your history...</p>
        ) : requests.length > 0 ? (
          requests.map(r => (
            <div key={r.id} className={styles.requestItem}>
              <div className={styles.reqInfo}>
                <h4>{r.type.replace('_', ' ').toUpperCase()}</h4>
                <p>{r.details}</p>
                <p style={{ fontSize: '0.75rem', marginTop: '0.25rem' }}>
                  Submitted on {new Date(r.created_at).toLocaleDateString()}
                </p>
              </div>
              <span className={`${styles.badge} ${styles[r.status]}`}>
                {r.status}
              </span>
            </div>
          ))
        ) : (
          <p style={{ color: '#64748b', fontStyle: 'italic' }}>No previous requests found.</p>
        )}
      </div>
    </div>
  );
}
