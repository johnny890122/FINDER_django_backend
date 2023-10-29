import { Routes, Route } from 'react-router-dom'
import { NavBar } from './components/NavBar'
import { Form } from './pages/Form'
import { Data } from './pages/Data'

const App = () => {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Form />} />
        <Route path="/data" element={<Data />} />
      </Routes>
    </>
  )
}

export default App
