import { Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { Tour } from './pages/Tour'
import { GameHome } from './pages/game'

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tour" element={<Tour />} />
        <Route path="/game" element={<GameHome />} />
      </Routes>
    </>
  )
}

export default App
