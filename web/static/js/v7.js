$(document).ready(function () {
  $("#sidebar1").mCustomScrollbar({
    theme: "minimal",
  });

  $("#sidebarCollapse").on("click", function () {
    // open or close navbar
    $("#sidebar1").toggleClass("active");
    // close dropdowns
    $(".collapse.in").toggleClass("in");
    // and also adjust aria-expanded attributes we use for the open/closed arrows
    // in our CSS
    $("a[aria-expanded=true]").attr("aria-expanded", "false");
  });
});

var dataurl = "data/movies.json";
var Fields = {
  categ: [
    "Creative_Type",
    "Director",
    "Distributor",
    "Major_Genre",
    "MPAA_Rating",
    "Source",
    "Title",
  ],
  date: ["Release_Date"],
  quant: [
    "IMDB_Rating",
    "IMDB_Votes",
    "Production_Budget",
    "Rotten_Tomatoes_Rating",
    "Running_Time_min",
    "US_DVD_Sales",
    "US_Gross",
    "Worldwide_Gross",
  ],
};

var bookmarkContent = document.querySelector(".bookmark_content");
var fieldLst = document.querySelector(".attr-lst");
var mainImg = document.querySelector(".mainImg");
var relatedImg = document.querySelector(".relatedImg");

var dfsRec = [];
var curDFSRecLen = 0;

// names of selected field
var checkedFields = [];
var queryMap = {};
var bookmarked = {};

initial();

function initial() {
  initField(Fields);
}

function addFields(fields) {
  let res = "";
  let enabledstr = "enabled";
  for (e of fields.categ) {
    res += `<li class="categ-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-font"></i> &nbsp;
                        <label class="form-check-label" for="${e}">
                           ${e}
                        </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}"/>
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.date) {
    res += `<li class="date-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-calendar-alt"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.quant) {
    res += `<li class="quant-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-hashtag"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }

  fieldLst.innerHTML += res;
}

function initField(fields) {
  fieldLst.innerHTML = "";
  addFields(fields);

  //adding event listeners to field labels
  let a = document.querySelectorAll("form .enabled div");
  for (i of a) {
    i.addEventListener("click", onClickEvent);
  }

  let modal = document.querySelector("#popup");
  let BMbtn = document.querySelector("#bookmark");
  let closeBtn = document.querySelector(".close");

  // When the user clicks on the button, toggle the modal
  BMbtn.addEventListener("click", () => {
    if (modal.style.display == "block") {
      modal.style.display = "none";
    } else {
      // when the window is displayed, plot charts in divs
      modal.style.display = "block";
      refreshBookmark();
    }
  });
  // When the user clicks on <span> (x), close the modal
  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });
  // When the user clicks anywhere outside of the modal, close it
  window.addEventListener("click", (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  });

  generateInitRecPlots();
}

function generateInitRecPlots() {
  var data = {
    data: JSON.stringify({
      fields: [],
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "js2pyFieldsV7",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      relatedImg.innerHTML = "";
      dfsRec = response.recVegalite;
      // console.log(dfsRec);
      for (var i = 0; i < dfsRec.length; i++) {
        for (let prop in dfsRec[i]) {
          let prop_str = JSON.stringify(prop).replace(/\W/g, "");
          relatedImg.innerHTML += `<div class='view_wrapper ${prop_str}_wrapper'><i class='fas fa-bookmark add_bm' added="false"></i><i class="fas fa-list-alt specify_chart"></i><div class="views cate" id='${prop_str}'></div></div>`;
          let VlSpec = dfsRec[i][prop];
          vegaEmbed(`#${prop_str}`, VlSpec);
          queryMap[prop_str] = VlSpec;
        }
      }
      document.querySelector(".loadmoreDiv").style.display = "none";
      chart_btns();
    },
  });
}

function onClickEvent(e) {
  let box = e.target;
  if (box != null) {
    let s = box.value;
    // if a box is checked after the click
    if (box.checked) {
      // if we can check more fields add the field in.
      // also add its parsed name to the list.
      if (checkedFields.length < 3) {
        checkedFields.push(s);
        // if we can not check more fields, alert it.
      } else {
        alert(`You have selected more than 3 fields!`);
        box.checked = false;
        return;
      }

      // if a box is unchecked after the click,
      // also remove its parsed name from the list.
    } else {
      checkedFields = checkedFields.filter(function (value, index, arr) {
        return value.localeCompare(s) != 0;
      });
      // if 0 fields are checked, display alternative message.
      if (checkedFields.length == 0) {
        mainImg.innerHTML = `No specified visualization yet. Start exploring by selecting fields on the Field panel or specifying a chart below.`;
        generateInitRecPlots();
        return;
      }
    }
    generatePlot(checkedFields, s, box);
  }
}

function refreshBookmark() {
  let arr = bookmarkContent.childNodes;
  let v1keys = [];
  let btnstrs = [];

  if (Object.keys(bookmarked).length == 0) {
    bookmarkContent.innerHTML =
      "Oops, you don't have any bookmark yet. Click on bookmark tags on charts to add a bookmark!";
  } else {
    bookmarkContent.innerHTML = "";
    for (key of Object.keys(bookmarked)) {
      let value = bookmarked[key];
      console.log(bookmarked);
      console.log(key);

      // creat div structure append to the popup window.
      bookmarkContent.innerHTML += `<div class="view_wrapper ${key}_wrapper_bm" ><i class="fas fa-bookmark add_bm" added="true"></i><div class="views cate" id="${key}_bm"></div></div>`;

      // plot the recommandation
      vegaEmbed(`#${key}_bm`, value);

      btnstrs.push(`.${key}_wrapper_bm i`);
      let btn = document.querySelector(`.${key}_wrapper_bm i`);

      // change color and attribute of bookmark.
      btn.style.color = "#ffa500";
      btn.setAttribute("added", "true");
    }
    // add event listener to new bookmark
    for (btn of btnstrs)
      document.querySelector(btn).addEventListener("click", toggleBookMark);
  }
}

function toggleBookMark(e) {
  let btn = e.target;
  let vis = e.target.parentElement;
  let str = vis.classList.item(1);
  // if the mark was checked, user want to uncheck it.
  if (btn.getAttribute("added") == "true") {
    // remove bookmark from pop up window
    let arr = bookmarkContent.childNodes;
    for (n of arr) {
      if (
        `${str}`
          .split("_wrapper")[0]
          .split("_bm")[0]
          .localeCompare(n.classList.item(1).split("_bm")[0]) == 0
      ) {
        bookmarkContent.removeChild(n);
      }
    }
    delete bookmarked[`${str.split("_wrapper")[0]}`];

    // change color and state of the plot in views
    let mark = document.querySelector(`.${str.split("_bm")[0]} i`);
    if (mark != null) {
      mark.style.color = "rgb(216, 212, 223)";
      mark.setAttribute("added", "false");
    }
    refreshBookmark();

    // if the mark is unchecked, user want to check it.
  } else {
    btn.style.color = "#ffa500";
    btn.setAttribute("added", "true");

    let splittedStr = `${str.split("_wrapper")[0]}`;

    bookmarked[splittedStr] = queryMap[splittedStr];
    refreshBookmark();
  }
}

function generatePlot(selectedFields, s, box) {
  console.log(selectedFields);
  var data = {
    data: JSON.stringify({
      fields: selectedFields,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "js2pyFieldsV7",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      if (response.status === "success") {
        console.log(response);
        var vlDict = response.actualVegalite;
        dfsRec = response.recVegalite;
        for (let prop in vlDict) {
          prop_str = prop.replace(/\W/g, "");
          mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${prop_str}_wrapper"><i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${prop_str}" id="main"></div></div>`;
          let VlSpec = vlDict[prop];
          vegaEmbed("#main", VlSpec);
          queryMap[prop_str] = VlSpec;
        }
        generateRecPlot();

        chart_btns();
      } else if (response.status === "empty") {
        alert(
          "Sorry, we cannot generate charts with the combination of selected fields."
        );
        checkedFields = checkedFields.filter(function (value, index, arr) {
          return value.localeCompare(s) != 0;
        });
        box.checked = false;
      }
    },
  });
}

function chart_btns() {
  // add event listeners to all bookmark buttons on the page
  let btns = document.querySelectorAll(".add_bm");
  for (btn of btns) {
    btn.addEventListener("click", toggleBookMark);
  }

  let specBtns = document.querySelectorAll(".specify_chart");
  for (sBtn of specBtns) {
    sBtn.addEventListener("click", specifyChart);
  }

  let wrappers = document.querySelectorAll(".view_wrapper");

  // change color and state of a bookmark if a wrapper is in the bookmark content.
  for (wrapper of wrappers) {
    let item = `${wrapper.classList.item(1).split("_wrapper")[0]}`;
    if (item in bookmarked) {
      wrapper.querySelector("i").style.color = "#ffa500";
      wrapper.querySelector("i").setAttribute("added", "true");
    }
  }
}

function generateRecPlot() {
  relatedImg.innerHTML = "";
  document.querySelector(".loadmoreDiv").style.display = "none";
  console.log(dfsRec);
  let maxNum = 5;
  if (maxNum > dfsRec.length) {
    maxNum = dfsRec.length;
  }
  for (var i = 0; i < dfsRec.length; i++) {
    for (var j = 0; j < dfsRec[i].length; j++) {
      for (let prop in dfsRec[i][j]) {
        let prop_str = JSON.stringify(prop).replace(/\W/g, "");
        let wrapper_str = prop_str + i.toString();
        relatedImg.innerHTML += `<div class='view_wrapper ${wrapper_str}_wrapper'><i class='fas fa-bookmark add_bm' added="false"></i><i class="fas fa-list-alt specify_chart"></i><div class="views cate" id='${wrapper_str}'></div></div>`;
        let VlSpec = dfsRec[i][j][prop];
        vegaEmbed(`#${wrapper_str}`, VlSpec);
        queryMap[wrapper_str] = VlSpec;
        if (j === dfsRec[i].length - 1) {
          relatedImg.innerHTML += `<hr class="dashed ${wrapper_str}_dashed">`;
        }
        if (i >= maxNum) {
          document.querySelector(`.${wrapper_str}_wrapper`).style.display =
            "none";
        }
        if (i >= maxNum && j === dfsRec[i].length - 1) {
          document.querySelector(`.${wrapper_str}_dashed`).style.display =
            "none";
        }
      }
    }
  }
  chart_btns();

  if (dfsRec.length > 5) {
    curDFSRecLen = 5;
    document.querySelector(".loadmoreDiv").style.display = "block";
    document
      .querySelector("#loadmoreBtn")
      .addEventListener("click", loadMoreRec);
  }
}

function loadMoreRec() {
  console.log("click loadmore.");
  let maxNum = curDFSRecLen + 5;
  if (maxNum >= dfsRec.length) {
    maxNum = dfsRec.length;
    document.querySelector(".loadmoreDiv").style.display = "none";
  }
  for (var i = 0; i < maxNum; i++) {
    for (var j = 0; j < dfsRec[i].length; j++) {
      for (let prop in dfsRec[i][j]) {
        let prop_str = JSON.stringify(prop).replace(/\W/g, "");
        let wrapper_str = prop_str + i.toString();
        document.querySelector(`.${wrapper_str}_wrapper`).style.display =
          "block";
        if (j === dfsRec[i].length - 1) {
          document.querySelector(`.${wrapper_str}_dashed`).style.display =
            "block";
        }
      }
    }
  }
  chart_btns();
  curDFSRecLen = maxNum;
}

function specifyChart(e) {
  let btn = e.target;
  let vis = e.target.parentElement;
  let str = vis.classList.item(1).split("_wrapper")[0];
  let vljson = queryMap[str];

  reassignFields(vljson);

  var data = {
    data: JSON.stringify({
      vljson: vljson,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "js2pySpecV7",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      dfsRec = response.recVegalite;

      mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${str}_wrapper"><i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${str}" id="main"></div></div>`;
      vegaEmbed("#main", vljson);
      generateRecPlot();
      chart_btns();
    },
  });
}

function reassignFields(vljson) {
  console.log(vljson);
  let all_boxes = document.querySelectorAll(".form-check-input");
  // console.log(all_boxes);

  let fields = [];

  for (let encode in vljson["encoding"]) {
    if ("field" in vljson["encoding"][encode]) {
      fields.push(vljson["encoding"][encode]["field"]);
    }
  }

  for (box of all_boxes) {
    // console.log(box.value);
    if (fields.includes(box.value)) {
      box.checked = true;
    } else {
      box.checked = false;
    }
  }
  checkedFields = fields;
}
