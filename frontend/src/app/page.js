import Image from "next/image";
import styles from "./page.module.css";
import Link from "next/link";

export default function Home() {
  return (
    <div className={styles.container}>
      {/* Background Image Overlay */}
      <div className={styles.bgImage}></div>
      <div className={styles.overlay}></div>

      <div className={styles.hero}>
        <div className={styles.glass_box}>
          <h2 className={styles.title}>Welcome to NidhiBank</h2>
          <p className={styles.description}>
            👉 Trusted Banking for a Digital Future
          </p>
          <div className={styles.cta_container}>
            <Link href="/login" className={styles.secondary_btn}>
              <span>🔐</span> Sign In
            </Link>
            <Link href="/signup" className={styles.primary_btn}>
              <span>➕</span> Open Account
            </Link>
          </div>
        </div>
      </div>


      <div className={styles.bg_shapes}>
        <div className={styles.shape1}></div>
        <div className={styles.shape2}></div>
        <div className={styles.shape3}></div>
      </div>
    </div>
  );
}
