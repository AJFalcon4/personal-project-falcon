import { useState } from "react"
import { SimpleGrid, VStack, Button, Heading } from "@chakra-ui/react"
import { Ticket, Users, Crown } from "lucide-react"
import { MotionBox } from "../components/Motion"
import { staggerContainer, staggerItem } from "../components/animations/fffAnimations"
import TicketCard from "../components/cards/TicketCard"
import PaymentModal from "../components/PaymentModal"
import { createOrder } from "../utilities"
import { primaryButtonStyles } from "../theme"


// Added staggered entrance animations for ticket cards
export default function TicketsPage() {
  const [showPaymentModal, setShowPaymentModal] = useState(false)
  const [order, setOrder] = useState(null)
  const [ticketA, setTicketA] = useState(0)
  const [ticketB, setTicketB] = useState(0)
  const [ticketC, setTicketC] = useState(0)

  const handleCheckout = async () => {
    const cart = { typeA: ticketA, typeB: ticketB, typeC: ticketC }

    try {
      const createdOrder = await createOrder(cart)
      setOrder(createdOrder)
      setShowPaymentModal(true)
    } catch {
      alert("Something went wrong with the payment.")
    }
  }

  return (
    <VStack align="stretch" spacing={6}>
      <Heading size="lg" color="text.primary">
        Tickets
      </Heading>

      <MotionBox
        as={SimpleGrid}
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        columns={{ base: 1, md: 3 }}
        spacing={10}
        alignItems="stretch"
      >
        <MotionBox variants={staggerItem}>
          <TicketCard
            title="General Admission"
            icon={<Ticket size={20} />}
            price="$250.00"
            setTicketQty={setTicketA}
            description="3 Days of TTRPGs, Tavern Feasts, Mixed Potions, Rare Merch, and Heroic Gift Bags."
          />
        </MotionBox>

        <MotionBox variants={staggerItem}>
          <TicketCard
            title="Community Ticket"
            icon={<Users size={20} />}
            price="$400.00"
            setTicketQty={setTicketB}
            description="All General Admission perks + Shared On-Site Stay."
          />
        </MotionBox>

        <MotionBox variants={staggerItem}>
          <TicketCard
            title="Master Upgrade"
            icon={<Crown size={20} />}
            price="$600.00"
            setTicketQty={setTicketC}
            description="All General Admission perks + Private chamber on-site."
          />
        </MotionBox>
      </MotionBox>

      <Button
        size="lg"
        {...primaryButtonStyles}
        alignSelf="flex-start"
        onClick={handleCheckout}
      >
        Continue to Payment
      </Button>

      {showPaymentModal && order && (
        <PaymentModal
          show={showPaymentModal}
          onClose={() => {
            setShowPaymentModal(false)
            setOrder(null)
          }}
          order={order}
        />
      )}
    </VStack>
  )
}