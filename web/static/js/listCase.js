/**
 * @author wongming.cn
 * @email byonecry@qq.com
 * @date 2015/11/22.
 */

var pageListShow = function () {
    var pageInfo = {}; // The json object to save page information

    var initPageInfo = function () {
        pageInfo.pageSize = 5;
        pageInfo.bufferSize = 10;
        pageInfo.currentPageNo = 1;
        pageInfo.totalDataNo = 0;
        pageInfo.pageNo = 0;
        pageInfo.pageData = [];
        pageInfo.arrayData = [];
        pageInfo.startIndex = 0;
        pageInfo.postUrl = "/case";
        pageInfo.postData = {"bufferSize": pageInfo.bufferSize, "startIndex":0}
    };

    var loadData = function () {
        pageInfo.arrayData = [];
        if (pageInfo.pageNo!=1) {
            var itemNumber = pageInfo.pageData.length;
            for (var i = 0, j = 0; i < itemNumber; i++) {
                if (!pageInfo.arrayData[j]) {
                    pageInfo.arrayData[j] = $.parseJSON('{"pageData": []}');
                }
                pageInfo.arrayData[j].pageData[i] = pageInfo.pageData[i];
                if (i % pageInfo.pageSize == pageInfo.pageSize - 1) {
                    j++;
                }
            }
        } else {
            pageInfo.arrayData[0] = {"pageData": pageInfo.pageData};
        };
    };

    var loadTemplate = function (json) {
        $("#list_totalDataNo").text(pageInfo.totalDataNo);
        $("#list_pageSize").val(pageInfo.pageSize);
        $("#list_currentPageNo").val(pageInfo.currentPageNo);
        $("#list_pageNo").text(pageInfo.pageNo);
        $("#list_container").hide();
        $("#list_container").html(TrimPath.processDOMTemplate("list_template", json));
        $("#list_container").show();
    };

    var changePageSize = function(pageSize){
        if (pageSize>0 && pageSize<= pageInfo.bufferSize){
            pageInfo.pageSize = pageSize;
        };
        pageInfo.currentPageNo = Math.floor(pageInfo.startIndex/pageInfo.pageSize+1);
        pageInfo.startPageNo = Math.floor(pageInfo.startIndex/pageInfo.pageSize+1);
        pageInfo.endPageNo = pageInfo.startPageNo+Math.ceil(pageInfo.pageData.length/pageInfo.pageSize)-1;
        pageInfo.pageNo = Math.ceil(pageInfo.totalDataNo/pageInfo.pageSize);
        loadData();
        loadTemplate(pageInfo.arrayData[0]);
    };

    var showFirstPage = function(){
        if (pageInfo.currentPageNo!=1) {
            if (pageInfo.startPageNo==1) {
                pageInfo.currentPageNo = 1;
                loadTemplate(pageInfo.arrayData[0]);
            }else{
                pageInfo.currentPageNo = 1;
                pageInfo.postData={"bufferSize": pageInfo.bufferSize, "startIndex": 0};
                showPage();
            };
        };
    };

    var showLastPage = function(){
        if (pageInfo.currentPageNo!=pageInfo.pageNo) {
            if (pageInfo.endPageNo==pageInfo.pageNo) {
                pageInfo.currentPageNo = pageInfo.endPageNo;
                loadTemplate(pageInfo.arrayData[pageInfo.endPageNo - pageInfo.startPageNo]);
            }else{
                pageInfo.currentPageNo = Math.ceil(pageInfo.totalDataNo/pageInfo.pageSize);
                pageInfo.postData={
                    "bufferSize": pageInfo.bufferSize,
                    "startIndex": (Math.ceil(pageInfo.totalDataNo/pageInfo.bufferSize) - 1) * pageInfo.bufferSize
                };
                showPage();
            };
        };
    };

    var showPrevPage = function(){
        if (pageInfo.currentPageNo!=1) {
            if (pageInfo.currentPageNo>pageInfo.startPageNo) {
                pageInfo.currentPageNo--;
                loadTemplate(pageInfo.arrayData[pageInfo.currentPageNo - pageInfo.startPageNo]);
            }else{
                pageInfo.currentPageNo--;
                var startIndex = (pageInfo.currentPageNo - pageInfo.bufferSize/pageInfo.pageSize) * pageInfo.pageSize;
                if (startIndex<0) {
                    startIndex = 0;
                };
                pageInfo.postData={
                    "bufferSize": pageInfo.bufferSize,
                    "startIndex": startIndex
                };
                showPage();
            };
        };
    };

    var showNextPage = function(){
        if (pageInfo.currentPageNo!=pageInfo.pageNo) {
            if (pageInfo.currentPageNo<pageInfo.endPageNo) {
                pageInfo.currentPageNo++;
                loadTemplate(pageInfo.arrayData[pageInfo.currentPageNo-pageInfo.startPageNo]);
            }else{
                pageInfo.currentPageNo++;
                pageInfo.postData={
                    "bufferSize": pageInfo.bufferSize,
                    "startIndex": (pageInfo.currentPageNo-1)* pageInfo.pageSize
                };
                showPage();
            };
        };
    };

    var toPageNo = function(pageNo){
        if (pageNo<1) {
            showFirstPage();
        } else if (pageNo >pageInfo.pageNo){
            showLastPage();
        } else if (pageNo == pageInfo.currentPageNo){
            //do nothing
        } else {
            pageInfo.currentPageNo = pageNo;
            if (pageInfo.currentPageNo>=pageInfo.startPageNo && pageInfo.currentPageNo<=pageInfo.endPageNo) {
                loadTemplate(pageInfo.arrayData[pageInfo.currentPageNo-pageInfo.startPageNo]);
            }else{
                var startIndex = Math.floor(pageNo*pageInfo.pageSize/pageInfo.bufferSize)*pageInfo.bufferSize;
                pageInfo.postData={
                    "bufferSize": pageInfo.bufferSize,
                    "startIndex": startIndex
                };
                showPage();
            };
        };
    };

    var showPage = function () {
        $.post(
            pageInfo.postUrl,
            pageInfo.postData,
            function(data){
                pageListData = data;
                //pageListData = dddd;
                pageInfo.pageData =  data.pageData;
                pageInfo.bufferSize = data.bufferSize;
                pageInfo.totalDataNo = data.totalDataNo;
                pageInfo.startIndex = data.startIndex;
                pageInfo.startPageNo = Math.floor(pageInfo.startIndex/pageInfo.pageSize+1);
                pageInfo.endPageNo = pageInfo.startPageNo+Math.ceil(pageInfo.pageData.length/pageInfo.pageSize)-1;
                pageInfo.pageNo = Math.ceil(pageInfo.totalDataNo/pageInfo.pageSize);
                //pageInfo.sortCondition = pageListData.sortCondition;
                loadData();
                loadTemplate(pageInfo.arrayData[pageInfo.currentPageNo - pageInfo.startPageNo]);
            },
            "json"
        );
    };

    var initPageListShow = function () {
        initPageInfo();
                $("#list_pageSize").change(function () {
            changePageSize($("#list_pageSize").val());
            return false;
        });
        $("#list_currentPageNo").change(function () {
            toPageNo($("#list_currentPageNo").val());
            return false;
        });
        $("#list_firstPage").on("click", function () {
            showFirstPage();
            return false;
        });
        $("#list_lastPage").on("click", function () {
            showLastPage();
            return false;
        });
        $("#list_prevPage").on("click", function () {
            showPrevPage();
            return false;
        });
        $("#list_nextPage").on("click", function () {
            showNextPage();
            return false;
        });
        showPage();
    };
    initPageListShow();
};
pageListShow();
