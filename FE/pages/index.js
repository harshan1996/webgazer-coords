import React, { useState } from 'react';
import styles from '@/styles/Home.module.css';

export default function Home() {
  const [result, setResult] = useState([]);

  function display(event) {
    let X = event.clientX;
    let Y = event.clientY;
    setResult([X, Y]);
  }

  return (
    <>
    {console.log(result)}
      {/* <h3>Find the coordinates of the cursor with JavaScript</h3> */}
      
      <div onClick={display} className={styles.fullSize}>
        Click anywhere on this area
        <div>
        <b>X-coordinate: </b> {result[0]} <br />
        <b>Y-coordinate: </b> {result[1]}
        </div>
        <div style={{position:"absolute",left:'200px',top:'100px',width:'5px',height:"5px",backgroundColor:"#ff0000",transformOrigin: "top left",
      transform: "translate(-50%, -50%)"}}></div>
      </div>

    </>
  );
}


