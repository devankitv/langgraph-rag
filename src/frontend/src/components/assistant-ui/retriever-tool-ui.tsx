"use client";

import { makeAssistantToolUI } from "@assistant-ui/react";
import { SearchIcon, FileTextIcon, CheckIcon, Loader2Icon } from "lucide-react";

type RetrieverArgs = {
  query: string;
};

type RetrieverResult = {
  result: string;
};

export const RetrieverToolUI = makeAssistantToolUI<RetrieverArgs, RetrieverResult>({
  toolName: "retriever_tool",
  render: ({ args, status, result }) => {

    if (status.type === "running") {
      return (
        <div className="flex items-center gap-3 rounded-lg bg-blue-50 p-4">
          <Loader2Icon className="h-5 w-5 animate-spin text-blue-600" />
          <div>
            <p className="text-sm font-medium text-blue-900">
              Searching for information...
            </p>
            <p className="text-xs text-blue-700">
              Query: "{args?.query || 'Unknown'}"
            </p>
          </div>
        </div>
      );
    }

    if (status.type === "incomplete" && status.reason === "error") {
      return (
        <div className="rounded-lg bg-red-50 p-4">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-red-500"></div>
            <span className="text-sm font-medium text-red-900">
              Search failed
            </span>
          </div>
          <p className="mt-1 text-xs text-red-700">
            Failed to search for: "{args?.query || 'Unknown'}"
          </p>
        </div>
      );
    }

    // Check if we have a result (either from status or from the tool call)
    const hasResult = result || (status.type === "complete" && args);

    if (!hasResult) {
      return (
        <div className="rounded-lg bg-gray-50 p-4">
          <div className="flex items-center gap-2">
            <SearchIcon className="h-4 w-4 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">
              retriever_tool
            </span>
          </div>
          <p className="mt-1 text-xs text-gray-600">
            Query: "{args?.query || 'Unknown'}"
          </p>
        </div>
      );
    }

    return (
      <div className="space-y-3">
        {/* Tool Call Card */}
        <div className="rounded-lg border bg-white p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
              <SearchIcon className="h-4 w-4 text-blue-600" />
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-semibold text-gray-900">
                retriever_tool
              </h4>
              <p className="text-xs text-gray-600">
                Query: "{args?.query || 'Unknown'}"
              </p>
            </div>
            <CheckIcon className="h-4 w-4 text-green-600" />
          </div>
        </div>

        {/* Results Card */}
        {result && (
          <div className="rounded-lg border bg-gray-50 p-4">
            <div className="mb-3 flex items-center gap-2">
              <FileTextIcon className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                Retrieved Information
              </span>
            </div>
            
            <div className="max-h-60 overflow-y-auto rounded border bg-white p-3">
              <pre className="whitespace-pre-wrap text-xs text-gray-800">
                {result.result}
              </pre>
            </div>
          </div>
        )}
      </div>
    );
  },
});
