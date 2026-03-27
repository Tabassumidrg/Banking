'use client';

import { useState, useEffect } from 'react';
import styles from './cards.module.css';

export default function CardsPage() {
  const [user, setUser] = useState(null);
  const [isFrozen, setIsFrozen] = useState(false);
  const [showFullDetails, setShowFullDetails] = useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const getCardNumber = (id) => `4400 ${id.toString().padStart(4, '0')} ${id.toString().padStart(4, '0')} 9988`;
  const mockExp = '12/28';
  const mockCVV = '123';

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>My Cards</h1>
          <p className={styles.subtitle}>View and manage your NidhiBank virtual cards</p>
        </div>
        <button className={styles.addCardBtn}>+ Add New Card</button>
      </header>

      <div className={styles.grid}>
        <div className={styles.cardSection}>
          <div className={`${styles.virtualCard} ${isFrozen ? styles.frozen : ''}`}>
            <div className={styles.cardHeader}>
              <div className={styles.bankName}>NidhiBank</div>
              <div className={styles.chip}></div>
            </div>
            
            <div className={styles.cardInfo}>
              <div className={styles.cardNumber}>
                {showFullDetails ? getCardNumber(user?.id || 0) : '•••• •••• •••• 9988'}
              </div>
              <div className={styles.cardMeta}>
                <div className={styles.metaItem}>
                  <span>HOLDER NAME</span>
                  <div className={styles.val}>{user?.full_name || 'Nidhi Member'}</div>
                </div>
                <div className={styles.metaItem}>
                  <span>EXPIRY</span>
                  <div className={styles.val}>{mockExp}</div>
                </div>
                {showFullDetails && (
                  <div className={styles.metaItem}>
                    <span>CVV</span>
                    <div className={styles.val}>{mockCVV}</div>
                  </div>
                )}
              </div>
            </div>

            <div className={styles.cardBrand}>VISA</div>
          </div>

          <div className={styles.cardActions}>
            <button className={styles.actionBtn} onClick={() => setShowFullDetails(!showFullDetails)}>
              {showFullDetails ? 'Hide Details' : 'Show Card Details'}
            </button>
            <button className={`${styles.actionBtn} ${isFrozen ? styles.unfreeze : styles.freeze}`} onClick={() => setIsFrozen(!isFrozen)}>
              {isFrozen ? 'Unfreeze Card' : 'Freeze Card'}
            </button>
          </div>
        </div>

        <div className={styles.settingsSection}>
          <h3 className={styles.sectionTitle}>Card Settings</h3>
          <div className={styles.settingItem}>
            <div className={styles.settingInfo}>
              <div className={styles.settingName}>Online Transactions</div>
              <div className={styles.settingDesc}>Enable/Disable internet payments</div>
            </div>
            <label className={styles.switch}>
              <input type="checkbox" defaultChecked />
              <span className={styles.slider}></span>
            </label>
          </div>

          <div className={styles.settingItem}>
            <div className={styles.settingInfo}>
              <div className={styles.settingName}>International Usage</div>
              <div className={styles.settingDesc}>Enable/Disable payments outside India</div>
            </div>
             <label className={styles.switch}>
              <input type="checkbox" />
              <span className={styles.slider}></span>
            </label>
          </div>

          <div className={styles.settingItem}>
            <div className={styles.settingInfo}>
              <div className={styles.settingName}>Contactless Payments</div>
              <div className={styles.settingDesc}>Enable tap-to-pay via NFC</div>
            </div>
             <label className={styles.switch}>
              <input type="checkbox" defaultChecked />
              <span className={styles.slider}></span>
            </label>
          </div>

          <div className={styles.limitBox}>
            <div className={styles.limitHeader}>
              <span>Daily Transaction Limit</span>
              <span>₹2,50,000</span>
            </div>
            <div className={styles.progressBar}>
              <div className={styles.progressFill} style={{ width: '40%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
