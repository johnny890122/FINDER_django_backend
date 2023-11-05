import { Link } from 'react-router-dom'
import styled from '@emotion/styled'
import { Button } from '@mui/material'

export const Home = () => {
  return (
    <StyledContainer>
      <StyledLink to="/tour">
        <Button>Tour</Button>
      </StyledLink>
      <StyledLink to="/game">
        <Button>Start</Button>
      </StyledLink>
    </StyledContainer>
  )
}

const StyledContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  height: 100vh;
`
const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;
`