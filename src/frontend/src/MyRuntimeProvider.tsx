
import type { ReactNode } from "react";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
  type ChatModelAdapter,
  type ThreadAssistantMessagePart,
} from "@assistant-ui/react";

const MyModelAdapter: ChatModelAdapter = {
  async *run({ messages, abortSignal }) {
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

    // Use the streaming endpoint
    const response = await fetch("http://localhost:8000/stream-with-tools", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
      signal: abortSignal,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle streaming response
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("No response body");
    }

    let streamedText = "";
    const toolCalls: any[] = [];
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6); // Remove 'data: ' prefix
            if (data && data !== '[DONE]') {
              try {
                const parsed = JSON.parse(data);
                
                if (parsed.type === 'tool_call') {
                  // Add tool call to our collection
                  toolCalls.push({
                    type: "tool-call",
                    toolCallId: parsed.data.id,
                    toolName: parsed.data.name,
                    args: parsed.data.args,
                    argsText: JSON.stringify(parsed.data.args, null, 2),
                  });
                  
                  // Yield message with tool calls
                  const content: ThreadAssistantMessagePart[] = [
                    ...toolCalls.map(tc => ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                    } as ThreadAssistantMessagePart)),
                  ];
                  
                  yield { content };
                } else if (parsed.type === 'tool_result') {
                  // Update the corresponding tool call with the result
                  const toolCall = toolCalls.find(tc => tc.toolCallId === parsed.data.toolCallId);
                  if (toolCall) {
                    const result = parsed.data.result;
                    toolCall.result = typeof result === 'object' && result.result ? result.result : result;
                  }
                  
                  // Yield updated message with tool calls and results
                  const content: ThreadAssistantMessagePart[] = [
                    ...toolCalls.map(tc => ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)),
                    ...(streamedText ? [{
                      type: "text",
                      text: streamedText,
                    } as ThreadAssistantMessagePart] : []),
                  ];
                  
                  yield { content };
                } else if (parsed.type === 'text') {
                  streamedText += parsed.data;
                  
                  // Yield message with tool calls and updated text
                  const content: ThreadAssistantMessagePart[] = [
                    ...toolCalls.map(tc => ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)),
                    {
                      type: "text",
                      text: streamedText,
                    } as ThreadAssistantMessagePart,
                  ];
                  
                  yield { content };
                }
              } catch (e) {
                // If JSON parsing fails, treat as plain text
                if (data && !data.includes('[Tool Call:')) {
                  streamedText += data;
                  
                  // Yield message with tool calls and updated text
                  const content: ThreadAssistantMessagePart[] = [
                    ...toolCalls.map(tc => ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)),
                    {
                      type: "text",
                      text: streamedText,
                    } as ThreadAssistantMessagePart,
                  ];
                  
                  yield { content };
                }
              }
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
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