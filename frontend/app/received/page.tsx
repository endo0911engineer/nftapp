'use client';

import { useState } from "react";
import ReceivedGiftsList from "../components/ReceivedGiftsList";

export default function ReceivedPage() {
    const [loading, setLoading] = useState(false);

    return (
        <div className="container">
            <h2>Received Gifts</h2>
            <ReceivedGiftsList loading={loading} setLoading={setLoading} />
        </div>
    );
}