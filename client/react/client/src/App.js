import './App.css';
import Cam from './Cam'
import Position from './Position'
import Page from './components/Page/Page'
import Canvas from './components/Canvas/Canvas'
import SideNav from './components/SideNav/SideNav'
import CommandForm from './components/CommandForm/CommandForm'



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
        <div><p>hello</p></div>
        <div><p>hello</p></div>
        <div><p>hello</p></div>
      </SideNav>
      <Canvas>
        <div style={{gridColumn: "span 6", paddingTop:"3vh", marginLeft: "auto", marginRight: "auto"}}>
          <div style={{width: "100%"}}><div><Cam /></div></div>
        </div>
        <div>&nbsp;</div>
        <div style={{gridRow: "span 3"}}><button className="secondary">Left</button></div>
        <div style={{gridColumn: "span 2"}}> <button onClick={() => {console.log("FORWARD")}}>Forward</button> </div>
        <div style={{gridRow: "span 3"}}><button>Right</button></div>
        <div>&nbsp;</div>

        <div>&nbsp;</div>
        <div style={{gridColumn: "span 2"}}> <button>Stop</button> </div>
        <div>&nbsp;</div>

        <div>&nbsp;</div>
        <div style={{gridColumn: "span 2"}}> <button>Backward</button> </div>
        <div>&nbsp;</div>
      </Canvas>
      

    </Page>
    </div>
  );
}

/**
      <Position />*/

export default App;
