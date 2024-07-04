import OpenAI from 'openai';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import readlineSync from 'readline-sync';
dotenv.config();

let messages = [{ role: 'system', content: 'You are a professional assistant?' }];
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

function getInput(promptMessage) {
    return readlineSync.question(promptMessage, {
        hideEchoBack: false, // The typed characters won't be displayed if set to true
    });
}

// Example dummy function hard coded to return the same weather
// In production, this could be your backend API or an external API
async function getCurrentWeather(location, unit) {
    if (location.toLowerCase().includes('tokyo')) {
        return JSON.stringify({ location: 'Tokyo', temperature: '10', unit: 'celsius' });
    } else if (location.toLowerCase().includes('san francisco')) {
        return JSON.stringify({
            location: 'San Francisco',
            temperature: '72',
            unit: 'fahrenheit',
        });
    } else if (location.toLowerCase().includes('paris')) {
        return JSON.stringify({
            location: 'Paris',
            temperature: '22',
            unit: 'fahrenheit',
        });
    } else {
        return JSON.stringify({ location, temperature: 'unknown' });
    }
}

async function runConversation(messages) {
    const tools = [
        {
            type: 'function',
            function: {
                name: 'get_current_weather',
                description: 'Get the current weather in a given location',
                parameters: {
                    type: 'object',
                    properties: {
                        location: {
                            type: 'string',
                            description: 'The city and state, e.g. San Francisco, CA',
                        },
                        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
                    },
                    required: ['location'],
                },
            },
        },
    ];

    try {
        const response = await openai.chat.completions.create({
            model: 'gpt-4-turbo-preview',
            messages: messages,
            tools: tools,
            tool_choice: 'auto', // auto is default, but we'll be explicit
        });
        const responseMessage = response.choices[0].message;
        console.log(response);
        // Step 2: check if the model wanted to call a function
        const toolCalls = responseMessage.tool_calls;
        if (!responseMessage.tool_calls) {
            return response;
        }
        // Step 3: call the function
        // Note: the JSON response may not always be valid; be sure to handle errors
        const availableFunctions = {
            get_current_weather: getCurrentWeather,
        };

        // Step 4: add message to the conversation
        messages.push(responseMessage);

        for (const toolCall of toolCalls) {
            const functionName = toolCall.function.name;
            const functionToCall = availableFunctions[functionName];
            const functionArgs = JSON.parse(toolCall.function.arguments);
            const functionResponse = await functionToCall(
                functionArgs.location,
                functionArgs.unit
            );
            // Step 5: add extended response to the conversation
            messages.push({
                tool_call_id: toolCall.id,
                role: 'tool',
                name: functionName,
                content: functionResponse,
            });
            // Step 6: generates an extended response
            try {
                const secondResponse = await openai.chat.completions.create({
                    model: 'gpt-4-turbo-preview',
                    messages: messages,
                });
                return secondResponse;
            } catch (e) {
                console.error(e);
            }
        }
    } catch (e) {
        console.error(e);
    }
}

const start = async () => {
    console.log('\n\n----------------------------------');
    console.log('          CHAT WITH AI 🤖   ');
    console.log('----------------------------------\n');
    console.log('\nBot: How can I help you?');

    while (true) {
        const input = getInput('You: ');
        if (input === 'x') {
            console.log('Goodbye!');
            process.exit();
        }
        messages.push({ role: 'user', content: input });
        const response = await runConversation(messages);
        console.log('Bot: ', response.choices[0].message.content);
    }
};

start();
