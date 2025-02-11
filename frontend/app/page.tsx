'use client';
import { authenticateWithMetaMask } from "./hooks/useMetaMaskAuth";
import styles from "./styles/HomePage.module.css";

export default function HomePage() {
  const handleAuth = async () => {
    const result = await authenticateWithMetaMask();
    if (result && result.success) {
      window.location.href = "./users";
    } else {
      alert("認証に失敗しました");
    }
  }

return (
    <div className={styles.container}>
      <h1 className={styles.title}>Welcome to NFT Gift Platform</h1>
      <p className={styles.subtitle}>
        Send unique gifts to your loved ones with the power of NFTs.
      </p>
      <button className={styles.button} onClick={handleAuth}>
        Sign Up / Log In with MetaMask
      </button>
      <div className={styles.footer}>
        Powered by Blockchain Technology
      </div>
    </div>
);
};