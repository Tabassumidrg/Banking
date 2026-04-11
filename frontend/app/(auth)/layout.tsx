import styles from './auth.module.css';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.authContainer}>
      {/* ─── Left: Branding Panel ─── */}
      <div className={styles.brandingPanel}>
        <div className={styles.brandingContent}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>
              <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7v2h20V7L12 2zm0 2.5L18.5 7h-13L12 4.5zM4 10v7c0 1.1.9 2 2 2h1v-9H4zm4 9h3v-9H8v9zm4 0h3v-9h-3v9zm4 0h1c1.1 0 2-.9 2-2v-7h-3v9zM2 22h20v-2H2v2z"/>
              </svg>
            </div>
            <span className={styles.logoText}>NexBank</span>
          </div>

          <h2 className={styles.brandingTagline}>
            Banking reimagined for the digital age
          </h2>
          <p className={styles.brandingDescription}>
            Experience seamless, secure, and intelligent banking. Manage your 
            finances with cutting-edge technology and world-class security.
          </p>

          <ul className={styles.featureList}>
            <li className={styles.featureItem}>
              <span className={styles.featureIcon}>🔒</span>
              Bank-grade encryption & 2FA security
            </li>
            <li className={styles.featureItem}>
              <span className={styles.featureIcon}>⚡</span>
              Instant transfers & real-time notifications
            </li>
            <li className={styles.featureItem}>
              <span className={styles.featureIcon}>📊</span>
              Smart analytics & spending insights
            </li>
            <li className={styles.featureItem}>
              <span className={styles.featureIcon}>🌍</span>
              Global access with zero hidden fees
            </li>
          </ul>
        </div>
      </div>

      {/* ─── Right: Form Panel ─── */}
      <div className={styles.formPanel}>
        {children}
      </div>
    </div>
  );
}
