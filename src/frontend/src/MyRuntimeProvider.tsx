
import type { ReactNode } from "react";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
  type ChatModelAdapter,
  type ThreadAssistantMessagePart,
} from "@assistant-ui/react";

const MyModelAdapter: ChatModelAdapter = {
  async run({ messages, abortSignal }) {
    // Extract the latest user message as the question
    const latestUserMessage = messages
      .filter(msg => msg.role === "user")
      .pop()?.content;

    if (!latestUserMessage) {
      throw new Error("No user message found");
    }

    // Convert message content to string if it's an array
    const question = Array.isArray(latestUserMessage) 
      ? latestUserMessage.map(item => item.type === "text" ? item.text : "").join("")
      : latestUserMessage;

    const result = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Send the question in the format expected by your API
      body: JSON.stringify({
        question,
      }),
      // if the user hits the "cancel" button or escape keyboard key, cancel the request
      signal: abortSignal,
    });

    const data = await result.json();
    
    if (!data.success) {
      throw new Error(data.error || "API request failed");
    }

    // Process the backend messages to create tool calls and final answer
    const processedMessages: ThreadAssistantMessagePart[] = [];
    
    // Find tool calls and results
    const toolCalls: any[] = [];
    const toolResults: any[] = [];
    
    for (const message of data.messages) {
      if (message.role === "assistant" && Array.isArray(message.content)) {
        for (const part of message.content) {
          if (part.type === "tool-call") {
            toolCalls.push(part);
          }
        }
      } else if (message.role === "tool" && Array.isArray(message.content)) {
        for (const part of message.content) {
          if (part.type === "tool-result") {
            toolResults.push(part);
          }
        }
      }
    }

    // Create tool call messages with results
    for (const toolCall of toolCalls) {
      const toolResult = toolResults.find(tr => tr.toolCallId === toolCall.toolCallId);
      
      processedMessages.push({
        type: "tool-call",
        toolCallId: toolCall.toolCallId,
        toolName: toolCall.toolName,
        args: toolCall.args,
        argsText: JSON.stringify(toolCall.args),
        result: toolResult?.result || undefined
      } as ThreadAssistantMessagePart);
    }

    // Find the final text answer
    const finalMessage = data.messages
      .filter((msg: any) => msg.role === "assistant")
      .reverse()
      .find((msg: any) => 
        Array.isArray(msg.content) && 
        msg.content.some((part: any) => part.type === "text")
      );

    if (finalMessage) {
      const textContent = finalMessage.content
        .filter((part: any) => part.type === "text")
        .map((part: any) => part.text)
        .join(" ");

      processedMessages.push({
        type: "text",
        text: textContent,
      } as ThreadAssistantMessagePart);
    }

    // Return the processed messages
    return {
      content: processedMessages,
    };
  },
};

export function MyRuntimeProvider({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  const runtime = useLocalRuntime(MyModelAdapter);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
    </AssistantRuntimeProvider>
  );
}