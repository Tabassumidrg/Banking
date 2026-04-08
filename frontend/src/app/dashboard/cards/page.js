'use client';

import { useState, useEffect } from 'react';
import styles from './cards.module.css';

export default function CardsPage() {
  const [user, setUser] = useState(null);
  const [cards, setCards] = useState([]);
  const [activeCardIndex, setActiveCardIndex] = useState(0);
  const [showFullDetails, setShowFullDetails] = useState(false);
  const [paymentAmount, setPaymentAmount] = useState('');
  const [paymentMerchant, setPaymentMerchant] = useState('Amazon.in');
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showOtpModal, setShowOtpModal] = useState(false);
  const [otpInput, setOtpInput] = useState('');
  const [generatedOtp, setGeneratedOtp] = useState('');
  const [toastMsg, setToastMsg] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      
      // Load saved cards or default
      const savedCards = localStorage.getItem(`cards_${parsedUser.id}`);
      if (savedCards) {
        setCards(JSON.parse(savedCards));
      } else {
        const defaultCard = {
          id: Date.now(),
          number: `4400 ${parsedUser.id.toString().padStart(4, '0')} ${parsedUser.id.toString().padStart(4, '0')} 9988`,
          exp: '12/28',
          cvv: '123',
          brand: 'VISA',
          isFrozen: false,
          transactions: []
        };
        setCards([defaultCard]);
      }
    }
  }, []);

  useEffect(() => {
    if (user && cards.length > 0) {
      // Ensure existing cards have a transactions array structure
      const validatedCards = cards.map(c => ({
        ...c,
        transactions: c.transactions || []
      }));
      localStorage.setItem(`cards_${user.id}`, JSON.stringify(validatedCards));
    }
  }, [cards, user]);

  const showToast = (message, duration = 5000) => {
    setToastMsg(message);
    setTimeout(() => setToastMsg(null), duration);
  };

  const handleAddCard = () => {
    const newCard = {
      id: Date.now(),
      number: `5200 ${Math.floor(Math.random() * 9000 + 1000)} ${Math.floor(Math.random() * 9000 + 1000)} ${Math.floor(Math.random() * 9000 + 1000)}`,
      exp: '06/30',
      cvv: Math.floor(Math.random() * 900 + 100).toString(),
      brand: cards.length % 2 === 0 ? 'MASTERCARD' : 'VISA',
      isFrozen: false,
      transactions: []
    };
    setCards([...cards, newCard]);
    setActiveCardIndex(cards.length);
    alert("New virtual card generated successfully!");
  };

  const handleRemoveCard = () => {
    if (cards.length <= 1) {
      alert("You must have at least one card active.");
      return;
    }
    if (confirm("Are you sure you want to remove this card? This action cannot be undone.")) {
      const updatedCards = cards.filter((_, i) => i !== activeCardIndex);
      setCards(updatedCards);
      setActiveCardIndex(0);
      setShowFullDetails(false);
    }
  };

  const toggleFreeze = () => {
    const updatedCards = [...cards];
    updatedCards[activeCardIndex].isFrozen = !updatedCards[activeCardIndex].isFrozen;
    setCards(updatedCards);
  };

  const currentCard = cards[activeCardIndex];

  const handleInitPayment = (e) => {
    e.preventDefault();
    const amount = parseFloat(paymentAmount);
    
    if (isNaN(amount) || amount <= 0) return;

    if (currentCard.isFrozen) {
      alert("This card is currently frozen! You cannot make payments until it is unfreezed.");
      return;
    }

    // Fraud Detection Logic: Anything over 1 Lakh INR is flagged as Fraud immediately
    if (amount > 100000) {
      const fraudTx = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        merchant: paymentMerchant,
        amount: amount,
        status: 'Blocked (Fraud Alert)'
      };
      
      const updatedCards = [...cards];
      updatedCards[activeCardIndex].transactions.unshift(fraudTx);
      updatedCards[activeCardIndex].isFrozen = true; // Auto freeze card
      setCards(updatedCards);
      
      alert(`⚠️ FRAUD ALERT: A suspicious transaction of ₹${amount.toLocaleString('en-IN')} was blocked. For your security, this card has been automatically frozen.`);
      setShowPaymentModal(false);
      setPaymentAmount('');
      return;
    }

    // Normal transaction triggers OTP
    const otp = Math.floor(1000 + Math.random() * 9000).toString();
    setGeneratedOtp(otp);
    setShowPaymentModal(false);
    setShowOtpModal(true);
    
    showToast(`NidhiBank SMS: Your OTP for payment of ₹${amount} at ${paymentMerchant} is ${otp}. Do not share this with anyone.`);
  };

  const handleVerifyOtp = () => {
    if (otpInput === generatedOtp) {
      const successTx = {
        id: Date.now(),
        date: new Date().toLocaleString(),
        merchant: paymentMerchant,
        amount: parseFloat(paymentAmount),
        status: 'Completed'
      };

      const updatedCards = [...cards];
      updatedCards[activeCardIndex].transactions.unshift(successTx);
      setCards(updatedCards);
      
      showToast(`✅ Payment of ₹${paymentAmount} to ${paymentMerchant} Successful!`);
      setShowOtpModal(false);
      setOtpInput('');
      setPaymentAmount('');
    } else {
      alert("Invalid OTP! Transaction failed.");
      setShowOtpModal(false);
      setOtpInput('');
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>My Cards</h1>
          <p className={styles.subtitle}>Manage your {cards.length} virtual NidhiBank cards</p>
        </div>
        <button className={styles.addCardBtn} onClick={handleAddCard}>+ Add New Card</button>
      </header>

      {cards.length > 1 && (
        <div className={styles.cardSelector}>
          {cards.map((c, i) => (
            <button 
              key={c.id} 
              className={`${styles.selectorBtn} ${activeCardIndex === i ? styles.activeSelector : ''}`}
              onClick={() => { setActiveCardIndex(i); setShowFullDetails(false); }}
            >
              Card {i + 1} ({c.brand})
            </button>
          ))}
        </div>
      )}

      {currentCard && (
        <div className={styles.grid}>
          <div className={styles.cardSection}>
            <div className={`${styles.virtualCard} ${currentCard.isFrozen ? styles.frozen : ''} ${currentCard.brand === 'MASTERCARD' ? styles.mastercardBg : ''}`}>
              <div className={styles.cardHeader}>
                <div className={styles.bankName}>NidhiBank</div>
                <div className={styles.chip}></div>
              </div>
              
              <div className={styles.cardInfo}>
                <div className={styles.cardNumber}>
                  {showFullDetails ? currentCard.number : `•••• •••• •••• ${currentCard.number.slice(-4)}`}
                </div>
                <div className={styles.cardMeta}>
                  <div className={styles.metaItem}>
                    <span>HOLDER NAME</span>
                    <div className={styles.val}>{user?.full_name || 'Card Holder'}</div>
                  </div>
                  <div className={styles.metaItem}>
                    <span>EXPIRY</span>
                    <div className={styles.val}>{currentCard.exp}</div>
                  </div>
                  {showFullDetails && (
                    <div className={styles.metaItem}>
                      <span>CVV</span>
                      <div className={styles.val}>{currentCard.cvv}</div>
                    </div>
                  )}
                </div>
              </div>

              <div className={styles.cardBrand}>{currentCard.brand}</div>
            </div>

            <div className={styles.cardActions}>
              <button className={styles.actionBtn} onClick={() => setShowFullDetails(!showFullDetails)}>
                {showFullDetails ? 'Hide Details' : 'Show Card Details'}
              </button>
              <button className={`${styles.actionBtn} ${currentCard.isFrozen ? styles.unfreeze : styles.freeze}`} onClick={toggleFreeze}>
                {currentCard.isFrozen ? 'Unfreeze Card' : 'Freeze Card'}
              </button>
              <button className={`${styles.actionBtn} ${styles.payBtn}`} onClick={() => setShowPaymentModal(true)}>
                Test Payment
              </button>
              <button className={`${styles.actionBtn} ${styles.removeBtn}`} onClick={handleRemoveCard}>
                Remove Card
              </button>
            </div>
          </div>

          <div className={styles.settingsSection}>
            <h3 className={styles.sectionTitle}>Card Settings (Card {activeCardIndex + 1})</h3>
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

            <div className={styles.txListContainer}>
              <h3 className={styles.sectionTitle}>Real-time Tracker (Card {activeCardIndex + 1})</h3>
              {currentCard?.transactions?.length > 0 ? (
                <div className={styles.txList}>
                  {currentCard.transactions.map(tx => (
                    <div key={tx.id} className={`${styles.txItem} ${tx.status.includes('Blocked') ? styles.txBlocked : styles.txCompleted}`}>
                      <div className={styles.txMain}>
                        <span className={styles.txMerchant}>{tx.merchant}</span>
                        <span className={styles.txAmount}>₹{tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                      </div>
                      <div className={styles.txMeta}>
                        <span className={styles.txDate}>{tx.date}</span>
                        <span className={styles.txStatus}>{tx.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className={styles.emptyTx}>No transactions tracked for this card yet.</div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Simulator Modals & Notifications */}
      {showPaymentModal && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <h2 className={styles.modalTitle}>Simulator: Online Payment</h2>
            <p className={styles.modalSub}>Test OTP and Fraud Detection logic.</p>
            <form onSubmit={handleInitPayment} className={styles.simForm}>
              <div className={styles.formGroup}>
                <label>Merchant Name</label>
                <select value={paymentMerchant} onChange={e => setPaymentMerchant(e.target.value)}>
                  <option value="Amazon.in">Amazon.in</option>
                  <option value="Flipkart">Flipkart</option>
                  <option value="Zomato">Zomato</option>
                  <option value="International Vendor Ltd">International Vendor Ltd</option>
                </select>
              </div>
              <div className={styles.formGroup}>
                <label>Amount (₹)</label>
                <input 
                  type="number" 
                  autoFocus
                  required
                  placeholder="e.g. 5000"
                  value={paymentAmount}
                  onChange={e => setPaymentAmount(e.target.value)}
                />
                <span className={styles.hint}>Testing Tip: Enter an amount &gt; ₹1,00,000 to trigger Fraud Alert.</span>
              </div>
              <div className={styles.modalActions}>
                <button type="button" className={styles.cancelBtn} onClick={() => setShowPaymentModal(false)}>Cancel</button>
                <button type="submit" className={styles.submitBtn}>Initiate Payment</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showOtpModal && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <div className={styles.otpHeader}>
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <h2 className={styles.modalTitle}>Authentication Required</h2>
              <p className={styles.modalSub}>To complete your ₹{paymentAmount} payment to {paymentMerchant}, enter the OTP sent to your registered mobile number.</p>
            </div>
            <div className={styles.otpInputGroup}>
              <input 
                type="text" 
                maxLength="4" 
                placeholder="• • • •" 
                value={otpInput}
                onChange={e => setOtpInput(e.target.value)}
                className={styles.otpInput}
                autoFocus
              />
            </div>
            <div className={styles.modalActions}>
              <button type="button" className={styles.cancelBtn} onClick={() => setShowOtpModal(false)}>Cancel</button>
              <button type="button" className={styles.verifyBtn} onClick={handleVerifyOtp} disabled={otpInput.length !== 4}>Verify & Pay</button>
            </div>
          </div>
        </div>
      )}

      {toastMsg && (
        <div className={styles.toastNotification}>
          <div className={styles.toastIcon}>💬</div>
          <div className={styles.toastContent}>{toastMsg}</div>
        </div>
      )}
    </div>
  );
}
