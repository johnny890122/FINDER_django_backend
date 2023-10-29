import { Link } from 'react-router-dom';
import styled from '@emotion/styled';
import { AppBar, Box, Toolbar, Container, Button } from '@mui/material';
import { menuSetting } from '../utils/menuSetting';

export const NavBar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <StyledBox>
            {menuSetting.map((page) => (
              <StyledMenuLink to={page.path}>
                <StyledMenuButton key={page.title}>
                  {page.title}
                </StyledMenuButton>
              </StyledMenuLink>
            ))}
          </StyledBox>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

const StyledBox = styled(Box)`
  display: flex;
  justify-content: flex-start;
`
const StyledMenuLink = styled(Link)`
  text-decoration: none;
  color: inherit;
`
const StyledMenuButton = styled(Button)`
  &.MuiButton-root {
    color: white;
    display: block;
  }
`