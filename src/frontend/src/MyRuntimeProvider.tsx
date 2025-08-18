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
      .filter((msg) => msg.role === "user")
      .pop()?.content;

    if (!latestUserMessage) {
      throw new Error("No user message found");
    }

    // Convert message content to string if it's an array
    const question = Array.isArray(latestUserMessage)
      ? latestUserMessage
          .map((item) => (item.type === "text" ? item.text : ""))
          .join("")
      : latestUserMessage;

    try {
      // Make API request to the backend
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      // Get the response reader for streaming
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Response body is not readable");
      }

      const decoder = new TextDecoder();
      let streamedText = "";
      const toolCalls: any[] = [];
      let buffer = ""; // Buffer for incomplete JSON strings

      // Read the stream
      while (true) {
        // Check for abort signal
        if (abortSignal?.aborted) {
          reader.cancel();
          break;
        }

        const { done, value } = await reader.read();
        if (done) break;

        // Decode the chunk and add it to our buffer
        buffer += decoder.decode(value, { stream: true });

        // Process complete lines from the buffer
        let lineEnd;
        while ((lineEnd = buffer.indexOf("\n")) >= 0) {
          const line = buffer.slice(0, lineEnd);
          buffer = buffer.slice(lineEnd + 1);

          if (!line.trim()) continue;

          try {
            const parsed = JSON.parse(line);

            if (parsed.type === "tool_call") {
              toolCalls.push({
                type: "tool-call",
                toolCallId: parsed.data.id,
                toolName: parsed.data.name,
                args: parsed.data.args,
                argsText: JSON.stringify(parsed.data.args, null, 2),
              });

              const content: ThreadAssistantMessagePart[] = [
                ...toolCalls.map(
                  (tc) =>
                    ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                    } as ThreadAssistantMessagePart)
                ),
              ];

              yield { content };
            } else if (parsed.type === "tool_result") {
              const toolCall = toolCalls.find(
                (tc) => tc.toolCallId === parsed.data.toolCallId
              );
              if (toolCall) {
                const result = parsed.data.result;
                toolCall.result =
                  typeof result === "object" && result.result
                    ? result.result
                    : result;
              }

              const content: ThreadAssistantMessagePart[] = [
                ...toolCalls.map(
                  (tc) =>
                    ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)
                ),
                ...(streamedText
                  ? [
                      {
                        type: "text",
                        text: streamedText,
                      } as ThreadAssistantMessagePart,
                    ]
                  : []),
              ];

              yield { content };
            } else if (parsed.type === "text") {
              streamedText += parsed.data;

              const content: ThreadAssistantMessagePart[] = [
                ...toolCalls.map(
                  (tc) =>
                    ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)
                ),
                {
                  type: "text",
                  text: streamedText,
                } as ThreadAssistantMessagePart,
              ];

              yield { content };
            } else if (parsed.type === "done") {
              const content: ThreadAssistantMessagePart[] = [
                ...toolCalls.map(
                  (tc) =>
                    ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)
                ),
                ...(streamedText
                  ? [
                      {
                        type: "text",
                        text: streamedText,
                      } as ThreadAssistantMessagePart,
                    ]
                  : []),
              ];

              yield { content };
            }
          } catch (e) {
            // If JSON parsing fails, treat as plain text
            if (line.trim()) {
              streamedText += line;

              const content: ThreadAssistantMessagePart[] = [
                ...toolCalls.map(
                  (tc) =>
                    ({
                      type: "tool-call",
                      toolCallId: tc.toolCallId,
                      toolName: tc.toolName,
                      args: tc.args,
                      argsText: tc.argsText,
                      result: tc.result,
                    } as ThreadAssistantMessagePart)
                ),
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
    } catch (error) {
      throw new Error(`API request failed: ${error}`);
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
