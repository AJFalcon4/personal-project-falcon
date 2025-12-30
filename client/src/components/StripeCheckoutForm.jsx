import React, { useState } from "react";
import { CardElement, useStripe, useElements } from "@stripe/react-stripe-js";

export default function StripeCheckoutForm({ clientSecret, userId, onSuccess }) {
    const stripe = useStripe();
    const elements = useElements();
    const [processing, setProcessing] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!stripe || !elements) return;

        setProcessing(true);

        try {
            const cardElement = elements.getElement(CardElement);
            if (!cardElement) {
                alert("Payment form is not ready. Please try again.");
                return;
            }

            const { error, paymentIntent } = await stripe.confirmCardPayment(
                clientSecret,
                {
                    payment_method: {
                        card: cardElement,
                    },
                }
            );

            if (error) {
                alert(error.message || "Payment failed.");
                return;
            }

            if (paymentIntent?.status === "succeeded") {
                alert("Payment successful!");
                onSuccess?.(paymentIntent);
            } else {
                alert(`Payment status: ${paymentIntent?.status ?? "unknown"}`);
            }
        } finally {
            setProcessing(false);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <CardElement />

            <button type="submit" disabled={!stripe || processing}>
                {processing ? "Processing..." : "Pay"}
            </button>
        </form>
    );
}
