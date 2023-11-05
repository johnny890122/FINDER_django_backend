import { useState } from 'react'
import styled from '@emotion/styled'
import { Button } from '@mui/material'
import graph from '../../assets/graph.png'

export const GameHome = () => {
  const [sessionInformation, setSessionInformation] = useState(null)

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  const handleClick = async ({ difficulty }) => {
    await fetch('http://localhost:8000/session/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include',
      body: JSON.stringify({ difficulty }),
    })
    .then(async res => {
        const data = await res.json()
        setSessionInformation(data)
      }
    )
  }

  if (!sessionInformation) {
    return (
      <StyledButtonsContainer>
        <Button onClick={() => handleClick({ difficulty: 'easy' })}>Easy</Button>
        <Button onClick={() => handleClick({ difficulty: 'medium' })}>Medium</Button>
        <Button onClick={() => handleClick({ difficulty: 'hard' })}>Hard</Button>
      </StyledButtonsContainer>
    )
  }

  return (
    <StyledGamePageContainer>
      <StyledSessionInformationContainer>
        Difficulty: {sessionInformation.difficulty}
        <br />
        Session ID: {sessionInformation.sessionId}
      </StyledSessionInformationContainer>
      <StyledQuitButton onClick={() => setSessionInformation(null)}>Quit</StyledQuitButton>
      <StyledImage $image={graph} />
    </StyledGamePageContainer>
  )  
}

const StyledButtonsContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  height: 100vh;
`
const StyledGamePageContainer = styled.div`
  padding: 2rem 4rem;
  position: relative;
`
const StyledSessionInformationContainer = styled.div`
  font-size: 1.25rem;
  line-height: 2rem;
`
const StyledQuitButton = styled(Button)`
  position: absolute;
  right: 4rem;
`
const StyledImage = styled.div`
  background-image: ${({ $image }) => `url(${$image});`};
  width: 80vw;
  height: 80vh;
`