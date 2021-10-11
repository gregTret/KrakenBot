import React from "react";

function Selection() {
    return (
      <div class="content">
        <h3>Kraken Bot</h3>
        <p>a python built api that trades crypto automatically</p>
        <form>
          <input id="krakenPublicKey" type="text" class="krakenInput" placeholder="enter kraken public api key"></input>
          <input id="krakenPrivateKey" type="text" class="krakenInput" placeholder="enter kraken private api key"></input>
        </form>
        <p>select coin(s) to trade</p>
        <select name="coins" id="coins" class="krakenSelect">
          <option>one</option>
        </select>
      </div>
    );
  }
  
export default Selection;