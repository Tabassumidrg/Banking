'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import styles from '../auth.module.css';

export default function SignUpPage() {
  const [form, setForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const update = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  // Password strength
  const getPasswordStrength = (pw: string) => {
    if (!pw) return { level: 0, label: '' };
    let score = 0;
    if (pw.length >= 6) score++;
    if (pw.length >= 10) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;

    if (score <= 1) return { level: 1, label: 'Weak' };
    if (score <= 2) return { level: 2, label: 'Fair' };
    if (score <= 3) return { level: 3, label: 'Good' };
    return { level: 4, label: 'Strong' };
  };

  const strength = getPasswordStrength(form.password);

  const validate = () => {
    const newErrors: Record<string, string> = {};
    if (!form.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!form.lastName.trim()) newErrors.lastName = 'Last name is required';
    if (!form.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      newErrors.email = 'Enter a valid email address';
    }
    if (!form.password) {
      newErrors.password = 'Password is required';
    } else if (form.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    if (!form.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    if (!agreeTerms) {
      newErrors.terms = 'You must agree to the terms';
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
    alert('Account created! (Backend integration pending)');
  };

  const strengthClass = (index: number) => {
    if (index >= strength.level) return styles.strengthBar;
    const mod = strength.level <= 1 ? '' : strength.level <= 3 ? styles.medium : styles.strong;
    return `${styles.strengthBar} ${styles.active} ${mod}`;
  };

  return (
    <div className={styles.formCard}>
      <div className={styles.formHeader}>
        <h1 className={styles.formTitle}>Create your account</h1>
        <p className={styles.formSubtitle}>Start your banking journey with NexBank</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit} noValidate>
        {/* Name Row */}
        <div className={styles.inputRow}>
          <div className={styles.inputGroup}>
            <label className={styles.inputLabel} htmlFor="signup-first">
              First Name
            </label>
            <input
              id="signup-first"
              type="text"
              className={`${styles.inputField} ${errors.firstName ? styles.inputError : ''}`}
              placeholder="John"
              value={form.firstName}
              onChange={(e) => update('firstName', e.target.value)}
              autoComplete="given-name"
            />
            {errors.firstName && <p className={styles.errorText}>⚠ {errors.firstName}</p>}
          </div>
          <div className={styles.inputGroup}>
            <label className={styles.inputLabel} htmlFor="signup-last">
              Last Name
            </label>
            <input
              id="signup-last"
              type="text"
              className={`${styles.inputField} ${errors.lastName ? styles.inputError : ''}`}
              placeholder="Doe"
              value={form.lastName}
              onChange={(e) => update('lastName', e.target.value)}
              autoComplete="family-name"
            />
            {errors.lastName && <p className={styles.errorText}>⚠ {errors.lastName}</p>}
          </div>
        </div>

        {/* Email */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel} htmlFor="signup-email">
            Email Address
          </label>
          <input
            id="signup-email"
            type="email"
            className={`${styles.inputField} ${errors.email ? styles.inputError : ''}`}
            placeholder="you@example.com"
            value={form.email}
            onChange={(e) => update('email', e.target.value)}
            autoComplete="email"
          />
          {errors.email && <p className={styles.errorText}>⚠ {errors.email}</p>}
        </div>

        {/* Password */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel} htmlFor="signup-password">
            Password
          </label>
          <div className={styles.passwordWrapper}>
            <input
              id="signup-password"
              type={showPassword ? 'text' : 'password'}
              className={`${styles.inputField} ${errors.password ? styles.inputError : ''}`}
              placeholder="Min 8 characters"
              value={form.password}
              onChange={(e) => update('password', e.target.value)}
              autoComplete="new-password"
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
          {form.password && (
            <div className={styles.passwordStrength}>
              <div className={styles.strengthBars}>
                {[0, 1, 2, 3].map((i) => (
                  <div key={i} className={strengthClass(i)} />
                ))}
              </div>
              <span className={styles.strengthText}>{strength.label}</span>
            </div>
          )}
          {errors.password && <p className={styles.errorText}>⚠ {errors.password}</p>}
        </div>

        {/* Confirm Password */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel} htmlFor="signup-confirm">
            Confirm Password
          </label>
          <div className={styles.passwordWrapper}>
            <input
              id="signup-confirm"
              type={showConfirm ? 'text' : 'password'}
              className={`${styles.inputField} ${errors.confirmPassword ? styles.inputError : ''}`}
              placeholder="Re-enter your password"
              value={form.confirmPassword}
              onChange={(e) => update('confirmPassword', e.target.value)}
              autoComplete="new-password"
            />
            <button
              type="button"
              className={styles.passwordToggle}
              onClick={() => setShowConfirm(!showConfirm)}
              aria-label={showConfirm ? 'Hide password' : 'Show password'}
            >
              {showConfirm ? '🙈' : '👁'}
            </button>
          </div>
          {errors.confirmPassword && (
            <p className={styles.errorText}>⚠ {errors.confirmPassword}</p>
          )}
        </div>

        {/* Terms */}
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            className={styles.checkbox}
            checked={agreeTerms}
            onChange={(e) => setAgreeTerms(e.target.checked)}
          />
          <span className={styles.termsText}>
            I agree to the{' '}
            <Link href="#" className={styles.termsLink}>Terms of Service</Link>
            {' '}and{' '}
            <Link href="#" className={styles.termsLink}>Privacy Policy</Link>
          </span>
        </label>
        {errors.terms && <p className={styles.errorText}>⚠ {errors.terms}</p>}

        {/* Submit */}
        <button
          type="submit"
          className={styles.submitButton}
          disabled={isSubmitting}
          id="signup-submit"
        >
          {isSubmitting ? 'Creating account...' : 'Create Account'}
        </button>

        {/* Divider */}
        <div className={styles.divider}>or sign up with</div>

        {/* Social Buttons */}
        <div className={styles.socialButtons}>
          <button type="button" className={styles.socialButton} id="signup-google">
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
          <button type="button" className={styles.socialButton} id="signup-apple">
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
        Already have an account?{' '}
        <Link href="/sign-in" className={styles.formFooterLink}>
          Sign in
        </Link>
      </p>
    </div>
  );
}
