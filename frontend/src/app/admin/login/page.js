'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from './admin-login.module.css';
import Link from 'next/link';

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://banking-backend-final.onrender.com';
      const res = await fetch(`${backendUrl}/api/auth/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Access Denied');
      }

      // Security Check: Only allow Admins or the Master Email on this portal
      const u = data.user;
      if (u.role !== 'admin' && u.email !== 'nidhi.sharma@nidhi.bank') {
        throw new Error('This portal is restricted to Branch Administrators only.');
      }

      // Store user and redirect to dashboard
      localStorage.setItem('user', JSON.stringify(u));
      router.push('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.bgImage}></div>
      <div className={styles.overlay}></div>

      <div className={styles.loginCard}>
        {/* Portal Toggle */}
        <div className={styles.portalToggle}>
          <Link href="/login" className={styles.toggleOption}>
            🏠 Personal Use
          </Link>
          <span className={`${styles.toggleOption} ${styles.toggleActive}`}>
            🏢 Management Portal
          </span>
        </div>

        <div className={styles.logoArea}>
          <div className={styles.logoIcon}>NB</div>
          <h1 className={styles.title}>NidhiBank</h1>
          <p className={styles.subtitle}>Branch Management Portal</p>
        </div>

        {error && <div className={styles.errorMsg}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.label} htmlFor="email">Admin ID (Email)</label>
            <input
              type="email"
              id="email"
              className={styles.input}
              placeholder="admin@nidhi.bank"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label} htmlFor="password">Security Password</label>
            <input
              type="password"
              id="password"
              className={styles.input}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className={styles.submitBtn} disabled={isLoading}>
            {isLoading ? 'Verifying Credentials...' : 'Authorize Login'}
          </button>
        </form>

        <div className={styles.footer}>
          Standard customer? <Link href="/login" className={styles.link}>Personal Banking Portal</Link>
        </div>
      </div>
    </div>
  );
}
