import styles from './dashboard.module.css';

export default function DashboardPage() {
  return (
    <div>
      <h1 style={{ marginBottom: '30px', fontSize: '24px', fontWeight: '600' }}>Dashboard Overview</h1>
      
      {/* Stats Grid */}
      <div className={styles.grid}>
        <div className={styles.statCard}>
          <span className={styles.cardLabel}>Total Balance</span>
          <span className={styles.cardValue}>$45,231.89</span>
          <span className={styles.cardTrend}>+2.4% from last month</span>
        </div>
        <div className={styles.statCard}>
          <span className={styles.cardLabel}>Monthly Income</span>
          <span className={styles.cardValue}>$12,400.00</span>
          <span className={styles.cardTrend}>+4.1% from last month</span>
        </div>
        <div className={styles.statCard}>
          <span className={styles.cardLabel}>Monthly Expenses</span>
          <span className={styles.cardValue}>$3,842.12</span>
          <span className={styles.cardTrend} style={{ color: '#f87171' }}>-1.2% from last month</span>
        </div>
      </div>

      <div className={styles.grid} style={{ gridTemplateColumns: '2fr 1.2fr' }}>
        {/* Recent Transactions */}
        <div className={styles.section}>
          <div className={styles.sectionTitle}>
            <span>Recent Transactions</span>
            <span style={{ fontSize: '12px', color: '#6366f1', cursor: 'pointer' }}>View all</span>
          </div>
          
          <div className={styles.transList}>
            <TransactionItem 
              name="Apple Store" 
              date="Oct 24, 2023" 
              amount="-$999.00" 
              type="tech"
            />
            <TransactionItem 
              name="Salary - Tech Corp" 
              date="Oct 21, 2023" 
              amount="+$6,200.00" 
              type="salary"
              positive
            />
            <TransactionItem 
              name="Starbucks Coffee" 
              date="Oct 20, 2023" 
              amount="-$15.40" 
              type="food"
            />
            <TransactionItem 
              name="Amazon Prime" 
              date="Oct 18, 2023" 
              amount="-$12.99" 
              type="sub"
            />
            <TransactionItem 
              name="Gym Membership" 
              date="Oct 15, 2023" 
              amount="-$45.00" 
              type="health"
            />
          </div>
        </div>

        {/* Quick Actions / Cards */}
        <div className={styles.section}>
          <div className={styles.sectionTitle}>Quick Transfer</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <div className={styles.avatar} style={{ width: '45px', height: '45px' }}>AM</div>
              <div className={styles.avatar} style={{ width: '45px', height: '45px' }}>SK</div>
              <div className={styles.avatar} style={{ width: '45px', height: '45px' }}>RW</div>
              <div className={styles.avatar} style={{ backgroundColor: '#6366f1', color: 'white', cursor: 'pointer' }}>+</div>
            </div>
            
            <input 
              type="text" 
              placeholder="Enter amount" 
              style={{ 
                background: 'rgba(255,255,255,0.05)', 
                border: '1px solid rgba(255,255,255,0.1)',
                padding: '12px',
                borderRadius: '12px',
                color: 'white',
                outline: 'none'
              }} 
            />
            
            <button style={{ 
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              border: 'none',
              padding: '14px',
              borderRadius: '12px',
              color: 'white',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'opacity 0.2s'
            }}>
              Send Money
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function TransactionItem({ name, date, amount, positive }) {
  return (
    <div className={styles.transItem}>
      <div className={styles.transInfo}>
        <div className={styles.transIcon}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="2" y="5" width="20" height="14" rx="2" />
            <line x1="2" y1="10" x2="22" y2="10" />
          </svg>
        </div>
        <div className={styles.transDetails}>
          <span className={styles.transName}>{name}</span>
          <span className={styles.transDate}>{date}</span>
        </div>
      </div>
      <span className={`${styles.transAmount} ${positive ? styles.amountPos : styles.amountNeg}`}>
        {amount}
      </span>
    </div>
  );
}
