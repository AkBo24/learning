require('dotenv').config();
const OpenAI = require('openai');
const readlineSync = require('readline-sync');

// Open AI configuration

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});
const PERSONA =
    'skilled stand-up comedian with a quick wit and charismatic presence, known for their clever storytelling and ability to connect with diverse audiences through humor that is both insightful and relatable.';
const MODEL_ENGINE = 'gpt-3.5-turbo-1106';
const MESSAGE_SYSTEM = `You are a ${PERSONA}. You have a knack for telling 1-2 sentence funny stories.`;
const messages = [{ role: 'system', content: MESSAGE_SYSTEM }];

// Get user input
function getInput(promptMessage) {
    return readlineSync.question(promptMessage, {
        hideEchoBack: false, // The typed characters won't be displayed if set to true
    });
}

async function main() {
    console.log('\n\n----------------------------------');
    console.log('          CHAT WITH AI 🤖   ');
    console.log('----------------------------------\n');
    console.log("type 'x' to exit the conversation");
    runConversation();
}

async function runConversation() {
    while (true) {
        const input = getInput('You: ');
        if (input === 'x') {
            console.log('Goodbye!');
            process.exit();
        }
        // generate completions
        const completions = await openai.chat.completions.create({
            model: MODEL_ENGINE,
            messages: messages,
            temperature: 1,
            max_tokens: 256,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
        });
        messages.push(completions.choices[0].message.content);
        console.log(completions.choices[0].message.content);
    }
}

main();
