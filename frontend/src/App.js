import './App.css'
import React, { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import axios from 'axios'
import { NavBar } from './components/NavBar'
import { Form } from './pages/Form'
import { Data } from './pages/Data'

const App = () => {
  const [testingData, setTestingData] = useState([])
  useEffect(() => {
    axios
      .get('http://localhost:8000/api/')
      .then((response) => response)
      .then((data) => {
        setTestingData(data['data']['test'])
      })
      .catch((err) => {
        console.log(err.message)
      })
  }, [])

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Form testingData={testingData} />} />
        <Route path="/data" element={<Data />} />
      </Routes>
    </>
  )
}

export default App
