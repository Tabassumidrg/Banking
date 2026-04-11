'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import styles from '../auth.module.css';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = () => {
    const newErrors: { email?: string; password?: string } = {};
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Enter a valid email address';
    }
    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    // TODO: Connect to FastAPI backend
    await new Promise((r) => setTimeout(r, 1500));
    setIsSubmitting(false);
    alert('Sign in successful! (Backend integration pending)');
  };

  return (
    <div className={styles.formCard}>
      <div className={styles.formHeader}>
        <h1 className={styles.formTitle}>Welcome back</h1>
        <p className={styles.formSubtitle}>Sign in to your NexBank account</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        {/* Email */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel} htmlFor="signin-email">
            Email Address
          </label>
          <input
            id="signin-email"
            type="email"
            className={`${styles.inputField} ${errors.email ? styles.inputError : ''}`}
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />
          {errors.email && <p className={styles.errorText}>⚠ {errors.email}</p>}
        </div>

        {/* Password */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel} htmlFor="signin-password">
            Password
          </label>
          <div className={styles.passwordWrapper}>
            <input
              id="signin-password"
              type={showPassword ? 'text' : 'password'}
              className={`${styles.inputField} ${errors.password ? styles.inputError : ''}`}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
            <button
              type="button"
              className={styles.passwordToggle}
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? '🙈' : '👁'}
            </button>
          </div>
          {errors.password && <p className={styles.errorText}>⚠ {errors.password}</p>}
        </div>

        {/* Options Row */}
        <div className={styles.formOptions}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              className={styles.checkbox}
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            />
            Remember me
          </label>
          <Link href="#" className={styles.forgotLink}>
            Forgot password?
          </Link>
        </div>

        {/* Submit */}
        <button
          type="submit"
          className={styles.submitButton}
          disabled={isSubmitting}
          id="signin-submit"
        >
          {isSubmitting ? 'Signing in...' : 'Sign In'}
        </button>

        {/* Divider */}
        <div className={styles.divider}>or continue with</div>

        {/* Social Buttons */}
        <div className={styles.socialButtons}>
          <button type="button" className={styles.socialButton} id="signin-google">
            <span className={styles.socialIcon}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            </span>
            Google
          </button>
          <button type="button" className={styles.socialButton} id="signin-apple">
            <span className={styles.socialIcon}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/>
              </svg>
            </span>
            Apple
          </button>
        </div>
      </form>

      {/* Footer */}
      <p className={styles.formFooter}>
        Don&apos;t have an account?{' '}
        <Link href="/sign-up" className={styles.formFooterLink}>
          Create one
        </Link>
      </p>
    </div>
  );
}
