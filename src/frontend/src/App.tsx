import './App.css'
import { Thread } from "@/components/assistant-ui/thread";
import { SearchToolUI } from './components/assistant-ui/search-tool-ui';

function App() {
  return (
    <>
      <div className="h-full">
        <Thread />
        <SearchToolUI/>
      </div>
    </>
  )
}

export default App

