'use client';

import { useEffect, useState } from 'react';
import MintForm from '../components/MintForm';
import ReceivedGiftsList from '../components/ReceivedGiftsList';
import styles from '../styles/UserPage.module.css';
import { useRouter } from 'next/navigation';

export default function UserPage() {
  const [loading, setLoading] = useState(false);
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuthentication = async () => {
      const res = await fetch("http://127.0.0.1:8000/api/check_authentication/", {
        credentials: "include",
      });
      const data = await res.json();
      console.log(data);

      if (data.authenticated) {
        setWalletAddress(data.walletAddress);
      } else {
        router.push("/"); //未ログインならリダイレクト
      }
    };

    checkAuthentication();
  }, [router]);

  const handleLogout = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/logout/", {
            method: "POST",
            credentials: "include",
        });

        if (response.ok) {
            alert("ログアウトしました。")
            window.location.href = "/";
        } else {
            alert("ログアウトに失敗しました。");
        }
    } catch (error) {
        console.error("ログアウトエラー：", error);
        alert("ログアウト中にエラーが発生しました。");
    }
  };

  return (
    <div className={styles.user_page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Your NFT Dashboard</h1>
        <p className={styles.subtitle}>Mint and manage your NFTs in style.</p>
        {walletAddress && (
            <button className={styles.logout_button} onClick={handleLogout}>
                Logout
            </button>
        )}
      </header>

      <div className={styles.main_content}>
        <section className={styles.mint_section}>
          <h2 className={styles.section_title}>Mint New NFT</h2>
          <MintForm />
        </section>

        <section className={styles.received_section}>
          <h2 className={styles.section_title}>Received Gifts</h2>
          <ReceivedGiftsList loading={loading} setLoading={setLoading} />
        </section>
       </div>
    </div>
  );
};