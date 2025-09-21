// AitoFresh Restaurant Knowledge Base
// This file contains information about AitoFresh for the AI assistant

const AitoFreshKnowledge = {
    restaurant: {
        name: "AitoFresh",
        location: "Helsinki City Center, CityCenter mall, 2nd floor",
        cuisine: "Poke Bowls and fresh, healthy meals",
        specialties: ["Poke Bowls", "Fresh ingredients", "Healthy options"],
        proteins: ["Fish", "Chicken", "Vegan options"]
    },

    hours: {
        "Monday-Friday": "11:00 - 21:00 (Lunch: 11:00 - 15:00)",
        "Saturday": "11:00 - 21:00",
        "Sunday": "12:00 - 19:00",
        note: "Kitchen closes 30 minutes before restaurant closing"
    },

    contact: {
        phone: "+358 50 5494185",
        email: "customer@aitofresh.fi"
    },

    services: {
        dineIn: true,
        takeout: true,
        lunchBuffet: true,
        preOrdering: true,
        onlinePayment: true
    },

    philosophy: [
        "Fresh ingredients and interactive service",
        "Bringing people together",
        "Caring for our planet"
    ],

    // Menu categories (to be populated with actual items)
    menuCategories: [
        "Poke Bowls",
        "Lunch Buffet",
        "À la carte",
        "Drinks"
    ],

    // Sample responses for common questions
    commonResponses: {
        greeting: "Welcome to AitoFresh! I'm Hana, your friendly assistant. We specialize in fresh poke bowls and healthy meals. How can I help you today?",

        location: "We're located in Helsinki City Center on the 2nd floor of CityCenter mall. Perfect for a quick healthy lunch or dinner!",

        hours: "We're open Monday-Friday 11:00-21:00 (lunch buffet until 15:00), Saturday 11:00-21:00, and Sunday 12:00-19:00. Our kitchen closes 30 minutes before closing time.",

        specialties: "Our specialty is fresh poke bowls with various proteins including fish, chicken, and delicious vegan options. We also have a popular lunch buffet!",

        healthyOptions: "Everything at AitoFresh is focused on fresh, healthy ingredients. Our poke bowls are perfect for a nutritious meal with high-quality proteins and fresh vegetables.",

        booking: "You can call us at +358 50 5494185 to make a reservation, or email customer@aitofresh.fi. We also offer pre-ordering for faster service!",

        payment: "We accept various payment methods including online payment for pre-orders. Very convenient for busy Helsinki residents!"
    }
};

// Helper function to get restaurant info
function getAitoFreshInfo(category) {
    return AitoFreshKnowledge[category] || null;
}

// Export for use in other files if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AitoFreshKnowledge;
}