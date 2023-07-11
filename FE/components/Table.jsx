import React, { useState,useEffect } from 'react'
import styles from "@/styles/Home.module.css"
import { fetchEventSource } from "@microsoft/fetch-event-source";


const Table = () => {
  const [dimensions, setDimensions] = useState([]);
  const [textInTheBoxes, setTextInTheBoxes] = useState([]);
 

  const renderTable = () => {

    const tableRows = [];
    const numRows = 4;
    const numColumns = 5;

    const textInTheBox=[];
    if (textInTheBoxes.length>0){console.log("TEXT IN THE CELLS=",textInTheBoxes)}


    for (let row = 0; row < numRows; row++) {
      const tableBoxes = [];

      for (let col = 0; col < numColumns; col++) {
        const BoxKey = row * numColumns + col;

        const singleBox=<td key={BoxKey} className={styles.box}>
                            <h2>{BoxKey + 1}</h2>
                        </td>

        tableBoxes.push(
          singleBox
        );

      }

      const rowKey = `row-${row}`;
      tableRows.push(<tr key={rowKey}>{tableBoxes}</tr>);

    }
    return <>{tableRows}</>;
  };
  useEffect(() => {
    const tableBoxes = document.querySelectorAll('td');
    console.log("TABLE BOXES=",tableBoxes);
    const textInTheBox = Array.from(tableBoxes, (box) => `${box.innerText} `);

    setTextInTheBoxes(textInTheBox);
  }, []);
  

  useEffect(() => {
    const dimensionsOfTheBox = [];

    const tableBoxes = document.querySelectorAll("td");

    const button_element=document.getElementById("button")
    const button_rect=button_element.getBoundingClientRect()

    tableBoxes.forEach((box) => {
      const rect = box.getBoundingClientRect();
      const coordinates = {
        top: rect.top,
        left: rect.left,
        bottom: rect.bottom,
        right: rect.right,
      };

      dimensionsOfTheBox.push([
        coordinates.left,
        coordinates.top,
        coordinates.right,
        coordinates.bottom,
      ]);
    });
    const button_coords=[button_rect.left,button_rect.top,button_rect.right,button_rect.bottom]
    dimensionsOfTheBox.push(button_coords)

    if (dimensionsOfTheBox.length === 21) {
      setDimensions(dimensionsOfTheBox);
    }
  }, []);

    // GETTING THE COORDS FROM THE BACKEND TO BE HIGHLIGHTED 

        const fetchBox = async () => {
        await fetchEventSource('http://127.0.0.1:5000/coord', {
            method: "POST",
            headers: {
            Accept: 'text/event-stream',
            'Content-Type': 'application/json', 
            },
            
            body:JSON.stringify([dimensions,textInTheBoxes]),

            onopen(res) {
            if (res.ok && res.status === 200) {
                    console.log('Connection made ', res)}
            else if (res.status >= 400 && res.status < 500 && res.status !== 429) {
                console.log('Client side error ', res)}
            },
            onmessage(event) {
            const result=JSON.parse(event.data)
            if (typeof(result[1])==="string"){

                let newCoord=result
                const dotElement = document.createElement('div');
                dotElement.style.position ='absolute';
                dotElement.style.top = `${newCoord[1]}px`;
                dotElement.style.left = `${newCoord[0]}px`;
                dotElement.style.height = '10px';
                dotElement.style.width = '10px';
                dotElement.style.backgroundColor = 'blue';
                dotElement.style.zIndex="9999"
                dotElement.style.borderRadius="50%"
                document.body.appendChild(dotElement);

            // After 1 second, remove the dot
            setTimeout(() => {
                document.body.removeChild(dotElement)
                }, 1000);
            }


            else if(typeof(result[1])==="object"){
                let highlightBox=result
                const element = document.createElement('div');
                element.style.position = 'absolute';
                element.style.top = `${highlightBox[1][1]}px`;
                element.style.left = `${highlightBox[1][0]}px`;
                element.style.height = highlightBox[1][3]<"950"?'21.4vh':'7.6vh';
                element.style.width =highlightBox[1][3]<"950"? '19.2vw':'10.8vw';
                element.style.border="solid black"

                // Add color to the element
                element.style.backgroundColor = 'rgb(5, 66, 74)';

                document.body.appendChild(element);

                // After 0.3 seconds, removing the color
                setTimeout(() => {
                document.body.removeChild(element)
                }, 300);

                const inputElement = document.getElementById('highlight-text');
                inputElement.value += result[0]!=null? highlightBox[0]:""
                } 

            },
            onclose() {
            console.log('Connection closed by the server');
            }
        });
        };


      useEffect(()=>{
        if (dimensions.length===21){
          console.log("DIMENSIONS=",dimensions);
          fetchBox()
        }
        
      },[dimensions])
    
  return (
    <div style={{position:"absolute"}}>
    <table style={{backgroundColor:"black"}}>
      <tbody>{renderTable()}</tbody>
    </table>
    {/* <input type="text" name="text" id="highlight-text" className={styles.textBox} /> */}
    <textarea name="text" id="highlight-text" cols="30" rows="10" className={styles.textBox}></textarea>
    <button id="button" className={styles.button}>END</button>
    </div>
  );
};

export default Table;
