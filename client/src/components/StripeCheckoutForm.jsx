import React, { useState } from "react";
import { PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { Button, VStack } from "@chakra-ui/react";
import { showErrorToast } from "./ui/showErrorToast";
import { showSuccessToast } from "./ui/showSuccessToast";
import { primaryButtonStyles } from "../theme";

export default function StripeCheckoutForm({ clientSecret, userId, onSuccess }) {
    const stripe = useStripe();
    const elements = useElements();
    const [processing, setProcessing] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!stripe || !elements) return;

        setProcessing(true);

        try {

            const { error, paymentIntent } = await stripe.confirmPayment({
                elements,
                redirect: "if_required"
            });

            if (error) {
                showErrorToast("Payment", error.message || "Payment failed.");
                return;
            }

            if (paymentIntent?.status === "succeeded") {
                showSuccessToast("Payment", "Payment successful!");
                onSuccess?.(paymentIntent);
            } else {
                showErrorToast("Payment", `Payment status: ${paymentIntent?.status ?? "unknown"}`);
            }
        } finally {
            setProcessing(false);
        }
    };

    return (
        <VStack as="form" onSubmit={handleSubmit} spacing={4} align="stretch">
            <PaymentElement />

            <Button 
                type="submit" 
                isDisabled={!stripe || !elements || processing}
                {...primaryButtonStyles}
                _disabled={{
                    opacity: 0.6,
                    cursor: "not-allowed",
                }}
            >
                {processing ? "Processing..." : "Pay"}
            </Button>
        </VStack>
    );
}