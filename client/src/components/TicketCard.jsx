import { Box, Heading, Text } from "@chakra-ui/react";
import { MotionBox } from "./Motion";

export default function TicketCard({ title, price, setTicketQty, description }) {
    return(
        <MotionBox 
            className="rounded-xl"
            bg="white"
            borderRadius="lg"
            boxShadow="md"
            margin="10"
            p="6"
            whileHover={{y:-4}}
            whileTap={{scale:0.98}}
            initial={{opacity:0, y:12}}
            animate={{opacity:1, y:0}}
            transition={{duration:0.25, ease:"easeOut"}}
            >
            <Box>
                <Heading size="md" mb="2" color="blackAlpha.800">
                    {title}
                </Heading>
                <Text color="gray.600">{description}</Text>
            </Box>
            <Box> 
              <Heading size="sm" mb="1" color="blackAlpha.800">{price}</Heading>
              <input type="number" 
                id="quantity" 
                name="quantity" 
                min="0"
                onChange={(e) => setTicketQty(e.target.value)}
                />
            </Box>
        </MotionBox>
    );
}