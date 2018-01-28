//https://stackoverflow.com/questions/19011861/is-there-a-float-input-type-in-html5
//Below is the html to insert when you click add constraint for each button
let seasHTML = `
<select name="seasons">
    <option value="xseason">Year</option>
    <option value="nseason">Player's (n)th Season</option>
    <option value="xbefore">Before (Year)</option>
    <option value="xafter">After (Year)</option>
    <option value="nbefore">Before Player's (n)th</option>
    <option value="nafter">After Player's (n)th</option>
</select>
<input type="number" name="seaNum" min="1" size="6">
<br>`;
let statHTML = `
Stat:
<select name="stat">
    <option value="Batting_Average">AVG</option>
    <option value="Home_Runs">HR</option>
    <option value="RBIs">RBI</option>
    <option value="Runs">R</option>
    <option value="Hits">H</option>
    <option value="Doubles">2B</option>
    <option value="Triples">3B</option>
    <option value="Games">GP</option>
    <option value="Plate_Appearances">PA</option>
    <option value="At_Bats">AB</option>
    <option value="Stolen_Bases">SB</option>
    <option value="Caught_Stealing">CS</option>
    <option value="Walks">BB</option>
    <option value="Strike_Outs">K</option>
    <option value="On_Base_Percentage">OBP</option>
    <option value="SLUGGING">SLG</option>
    <option value="OPS">OPS</option>
    <option value="OPS_Plus+">OPS+</option>
    <option value="Total_Bases">TB</option>
    <option value="Double_Plays_Grounded_Into">GIDP</option>
    <option value="Hit_By_Pitch">HBP</option>
    <option value="Sacrifice_Hits">SAC</option>
    <option value="Sacrifice_Flies">SF</option>
    <option value="Intentional_Bases_On_Balls">IBB</option>
</select>
Constraint:
<select name="statconstraint">
    <option value="="> = </option>
    <option value=">"> > </option>
    <option value="<"> < </option>
</select>
<input type="number" name="statNum"  step="0.001" size="6">
<br>`;
let nameHTML = `
Constraint:
<select name="name">
    <option value="includes">Includes</option>
    <option value="starts">Starts With</option>
</select>
<input type="text" name="nameConst">
<br>`;
let posHTML = `
Type:
<select name="posType">
    <option value="include">Include</option>
    <option value="exclude">Exclude</option>
</select>
Position:
<select name="pos">
    <option value="1">P</option>
    <option value="2">C</option>
    <option value="3">1B</option>
    <option value="4">2B</option>
    <option value="5">3B</option>
    <option value="6">SS</option>
    <option value="7">LF</option>
    <option value="8">CF</option>
    <option value="9">RF</option>
    <option value="if">IF</option>
    <option value="of">OF</option>
</select>
<br>`;
let teamHTML = `
Type:
<select name="teamType">
    <option value="include">Include</option>
    <option value="exclude">Exclude</option>
</select>
Team/League:
<select name="team">
    <option value="0">All</option>
    <option value="AL">AL</option>
    <option value="NL">NL</option>
    <option value="AA">AA</option>
    <option value="NA">NA</option>
    <option value="UA">UA</option>
    <option value="PL">PL</option>
    <option value="BAL">BAL</option>
    <option value="BOS">BOS</option>
    <option value="NYY">NYY</option>
    <option value="TB">TB</option>
    <option value="TOR">TOR</option>
    <option value="CLE">CLE</option>
    <option value="CWS">CWS</option>
    <option value="DET">DET</option>
    <option value="KC">KC</option>
    <option value="MIN">MIN</option>
    <option value="HOU">HOU</option>
    <option value="LAA">LAA</option>
    <option value="OAK">OAK</option>
    <option value="SEA">SEA</option>
    <option value="TEX">TEX</option>
    <option value="ATL">ATL</option>
    <option value="MIA">MIA</option>
    <option value="NYM">NYM</option>
    <option value="PHI">PHI</option>
    <option value="WAS">WAS</option>
    <option value="CHC">CHC</option>
    <option value="CIN">CIN</option>
    <option value="MIL">MIL</option>
    <option value="PIT">PIT</option>
    <option value="STL">STL</option>
    <option value="ARI">ARI</option>
    <option value="COL">COL</option>
    <option value="LAD">LAD</option>
    <option value="SD">SD</option>
    <option value="SF">SF</option>
</select>
<br>`

// Determine which add constraint was hit and add appropriate html
function addConst(type){
    let old = $("#"+type+"Constraints").html();
    let html = "";
    if (type == "seas")
        html = seasHTML;
    if (type == "stat")
        html = statHTML;
    if (type == "name")
        html = nameHTML;
    if (type == "pos")
        html = posHTML;
    if (type == "team")
        html = teamHTML;
    $("#"+type+"Constraints").html(old + html);
}

// Determin which remove constraints was hit and update the html
function remConst(type){
    let old = $("#"+type+"Constraints").html();
    let html = "";
    if (type == "seas")
        html = seasHTML;
    if (type == "stat")
        html = statHTML;
    if (type == "name")
        html = nameHTML;
    if (type == "pos")
        html = posHTML;
    if (type == "team")
        html = teamHTML;
    $("#"+type+"Constraints").html(old - html);
}