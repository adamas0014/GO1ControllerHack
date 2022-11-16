import './App.css';
import Cam from './Cam'
import Position from './Position'
import Page from './components/Page/Page'
import Canvas from './components/Canvas/Canvas'
import SideNav from './components/SideNav/SideNav'
import CommandForm from './components/CommandForm/CommandForm'
import ControlPad from './components/ControlPad/ControlPad';
import ModeSwitcher from './components/ModeSwitcher/ModeSwitcher';
import NavButton from './components/NavButton/NavButton';


function App() {


  return (
    <div>

    <Page>
      <SideNav>
        <div>
          <a href="#"><div className="logo">&nbsp;</div></a>
        </div>
        <div className="heading" >
            GO1 Hack Studio
        </div>
        <CommandForm />
        <ModeSwitcher />
        <div style={{height: "2vh"}}></div>
        <NavButton name="Project Information" />
        <NavButton name="Project Website" />
        <NavButton name="GitHub" />

      </SideNav>
      <Canvas>
        <div style={{gridColumn: "span 6", paddingTop:"3vh", marginLeft: "auto", marginRight: "auto"}}>
          <div style={{width: "100%"}}><div><Cam /></div></div>
        </div>
        <ControlPad />
      </Canvas>
      

    </Page>
    </div>
  );
}

/**
      <Position />*/

export default App;
