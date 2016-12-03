var curBubId = '';

var mainTabSpans = new Array();

function initMainTabs() {
    var mainTabDiv = document.getElementById('main_tab');
    var cnt = 0;
    for (var i = 0; i < mainTabDiv.childNodes.length; i++) {
        if (mainTabDiv.childNodes[i].nodeName == 'SPAN') {
            mainTabSpans[cnt++] = mainTabDiv.childNodes[i];
        }
    }
}

function showMainTab(tabId) {
    if (tabId == 0) {
        document.getElementById('link_result').style.display = 'block';
        document.getElementById('chart').style.display = 'none';

        mainTabSpans[0].className = 'sel_tab_span';
        mainTabSpans[1].className = 'tab_span';
    } else {
        document.getElementById('link_result').style.display = 'none';
        document.getElementById('chart').style.display = 'block';

        mainTabSpans[0].className = 'tab_span';
        mainTabSpans[1].className = 'sel_tab_span';
    }
}

function stopEvent(ev) {
    ev.stopPropagation();
}

function demoEdlInit() {
    $('.marked_span').bind('click', showBubble);
    $('a[href="#info_link"]').on('shown.bs.tab', function(e) {
        $('.shape').css('display', 'inline-block');
    });
    $('a[href="#info_link"]').on('hidden.bs.tab', function(e) {
        $('.shape').css('display', 'none');
    });
}

function demoSfInit() {
    $('.marked_sf_sent').bind('click', showSlotBubble);
}

function showRelationHead(id) {
    var info_head = 'Drug-induced diseases'
    var e_color = 'rgb(224, 88, 85)';
    $('#sf_infobox').css('border-radius', '0 0 4px 4px');
    $('#info_entity_head').html(info_head);
    $('#info_entity_head').css('display', 'block');
    $('#info_entity_head').css('background-color', e_color);
    $('#info_entity_head').css('border-color', e_color);

    if (id) {
        $('#sf_new_edit #addf').attr('value', id);
        $('#sf_new_edit #removef').attr('value', id);
    }
}

function showSlotBubble(e) {
    $('#info_subj').html('<span>' + $(this).find('.marked_subj').text() + '</span>');
    $('#info_obj').html('<span>' + $(this).find('.marked_obj').text() + '</span>');
    $('#info_subj').addClass('editable');
    $('#info_obj').addClass('editable');

    showRelationHead(this.id);

    $('.editable').editable();
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function showEntityInfohead(id) {
    var e_text = $(id).text().replace($(id).find('sup').text(), '');
    var type = $(id).attr('class').split(' ')[2].split('_')[1];
    var e_class = capitalizeFirstLetter(type);
    if ($(id).attr('class').indexOf('newe') > -1) {
        e_class += '(new)';
        $('#edl_new_edit').css('display', 'block');
        $('#edl_new_edit #adde').attr('name', type);
        $('#edl_new_edit #adde').attr('value', e_text);
        $('#edl_new_edit #removee').attr('name', type);
        $('#edl_new_edit #removee').attr('value', e_text);
    } else {
        $('#edl_new_edit').css('display', 'none');
    }
    $('#edl_infobox').css('border-radius', '0 0 4px 4px');
    var e_color = $(id).css('color');
    var entity_name = '<div>' + e_class + ': <span style="border-bottom: 1px dotted;"><b><i>' + e_text + '</i></b></span></div>';
    $('#edl_infobox .infohead').attr('id', id);
    $('#info_entity_head').html(entity_name);
    $('#info_entity_head').css('display', 'block');
    $('#info_entity_head').css('background-color', e_color);
    $('#info_entity_head').css('border-color', e_color);
}

function showBubble(e) {
    e.stopPropagation();
    // $('a[href="#info_tree"]').tab;
    $('#edl_infobox .infohead li>a:first').tab('show');
    idx = this.id.split('_')[1];
    bubId = '#bub_' + idx;

    var divs = $(bubId).children();
    for (var i = 0; i < divs.length; ++i) {
        var type = divs[i].id.substr(1);
        var boxId = 'info_' + type;
        if (type == "tree") {
            try {
                var tree_data = JSON.parse(divs[i].innerText);
                // var tooltip_data = tree_data['tooltip'];
                // tree_data = tree_data['tree'];
                if (tree_data['mesh'].length > 0) {
                    $('#meshTree').treeview({
                        data: tree_data['mesh'],
                        levels: 10,
                        enableLinks: true,
                        collapseIcon: 'fa fa-minus',
                        expandIcon: 'fa fa-plus'
                    });
                } else {
                    $('#meshTree').treeview({
                        data: [{ 'text': 'N/A' }],
                        collapseIcon: 'fa fa-minus',
                        expandIcon: 'fa fa-plus'
                    });
                }
                if (tree_data['wiki'].length > 0) {
                    $('#wikiTree').treeview({
                        data: tree_data['wiki'],
                        levels: 10,
                        enableLinks: true,
                        collapseIcon: 'fa fa-minus',
                        expandIcon: 'fa fa-plus'
                    });
                } else {
                    $('#wikiTree').treeview({
                        data: [{ 'text': 'N/A' }],
                        collapseIcon: 'fa fa-minus',
                        expandIcon: 'fa fa-plus'
                    });
                }
                treeNodeClass = 'div.treeview ul li';
                $(treeNodeClass).attr('data-toggle', 'tooltip');
                $(treeNodeClass).each(function(e) {
                    var tip = $(this).find('a').attr('href')
                    if (tip) {
                        $(this).attr('title', tip.split('#')[1]);
                    }
                    return false;
                });
                $(treeNodeClass).tooltip();
            } catch (err) {
                console.log(err.message);
            }
        } else if (type == "syno") {
            var default_syno = '<ul class="list-group">' + '<li class="list-group-item">N/A</li></ul>'
            $('#meshSyno').html($(bubId).find('#mesh').html() || default_syno);
            $('#chebiSyno').html($(bubId).find('#chebi').html() || default_syno);
            $('#wikiSyno').html($(bubId).find('#wiki').html() || default_syno);
        } else if (type == "desc") {
            showEntityInfohead('#' + this.id);
            document.getElementById(boxId).innerHTML = divs[i].innerHTML;
        } else {
            document.getElementById(boxId).innerHTML = divs[i].innerHTML;
        }
    }
    $('.editable').editable();
}

function showSlotFillingResult() {
    showRelationHead();
    $('#edl_result_div').css('display', 'none');
    $('#sf_result_div').css('display', 'block');
    demoSfInit();
}

function showEntityLinkingResult() {
    $('#info_entity_head').css('display', 'none');
    $('#sf_result_div').css('display', 'none');
    $('#edl_result_div').css('display', 'block');
    demoEdlInit();
}

function highlight(id) {
    var e_class = '.marked_span.et_' + id.split('_')[1];
    // console.log(e_class);
    $(e_class).addClass('highlight');
    $('.marked_span.highlight').hover(function(e) {
        var targetEidx = $(this).find('sup').text();
        $('.marked_span').each(function(e) {
            var eidx = $(this).find('sup').text();
            if (eidx == targetEidx) {
                $(this).addClass("hovered");
            }
        })
        return false;
    }, function(e) {
        var targetEidx = $(this).find('sup').text();
        $('.marked_span').each(function(e) {
                var eidx = $(this).find('sup').text();
                if (eidx == targetEidx) {
                    $(this).removeClass("hovered");
                }
            })
            // var e_class = 'span.' + this.className.split(' ')[2];
        return false;
    });
    // $('.marked_span.highlight').on('mouseover', function(e) {
    //     console.log(this.className);
    //     $('.et_disease').toggleClass('hovered');
    //     return false;
    // });
    // $('.marked_span.highlight').on('mouseout', function(e) {
    //     console.log(this.className);
    //     $('.et_disease').toggleClass('hovered');
    //     return false;
    // });
}

function unhighlight(id) {
    var e_class = '.marked_span.et_' + id.split('_')[1];
    $(e_class).removeClass('highlight');
}

var dealEdlStateChange = function(e) {
    // console.log('I\'m in!!!')
    if ($(this).hasClass('active')) {
        console.log(this.id, 'I\'m activated!');
        // highlight entity
        showEntityLinkingResult();
        highlight(this.id);
        // $('.marked_span').addClass('highlight');
        // disable slot filling highlight
        $('#sf_infobox').css('display', 'none');
        $('#edl_infobox').css('display', 'block');
        var head_id = $('#edl_infobox .infohead').attr('id');
        if (head_id && head_id != "info_empty") {
            showEntityInfohead(head_id);
        }
        if ($('#demo_sf').hasClass('active')) {
            $('#demo_sf').removeClass('active').button('reset').trigger('change');
        }
    } else {
        console.log(this.id, 'I\'m deactivated!');
        // disable entity highlighting
        unhighlight(this.id);
    }
    return false;
};

var dealSfStateChange = function(e) {
    if ($(this).hasClass('active')) {
        // $.fn.editable.defaults.mode = 'modal';
        // $('#tags').editable({
        //     inputclass: 'input-large',
        //     select2: {
        //         tags: ['hello', 'world'],
        //         tokenSeparators: [",", " "]
        //     }
        // });
        // highlight sentences
        console.log(this.id, 'I\'m activated!');
        showSlotFillingResult();
        $('.marked_sf_sent').removeClass('unhighlight');
        $('#edl_infobox').css('display', 'none');
        $('#sf_infobox').css('display', 'block');
        // disable entity highlighting
        $('.demo_edl').each(function(e) {
            if ($(this).hasClass('active')) {
                $(this).removeClass('active').button('reset').trigger('change');
            }
        });
    } else {
        console.log(this.id, 'I\'m deactivated!');
        // disable sentence highlighting
        $('.marked_sf_sent').addClass('unhighlight');
    }
    return false;
};

// TABS
var tabLinksArr = new Array();
var contentDivsArr = new Array();

function resetTabs(idx) {
    // Assign onclick events to the tab links, and
    // highlight the first tab
    tabLinks = tabLinksArr[idx];
    contentDivs = contentDivsArr[idx];
    var i = 0;
    for (var id in tabLinks) {
        if (i == 0) {
            tabLinks[id].className = 'selected';
        } else
            tabLinks[id].className = '';
        i++;
    }

    // Hide all content divs except the first
    var i = 0;

    for (var id in contentDivs) {
        if (i != 0)
            contentDivs[id].className = 'tabContent hide';
        else
            contentDivs[id].className = 'tabContent';
        i++;
    }
}

function initTabUL(idx, tabUL, tabLinks, contentDivs) {
    var tabListItems = tabUL.childNodes;
    for (var i = 0; i < tabListItems.length; i++) {
        if (tabListItems[i].nodeName == "LI") {
            var tabLink = getFirstChildWithTagName(tabListItems[i], 'SPAN');
            var id = getTabContentId(tabLink.id);
            tabLinks[id] = tabLink;
            tabLinks[id].onclick = function() { showTab(this, idx); };
            tabLinks[id].onfocus = function() { this.blur() };
            contentDivs[id] = document.getElementById(id);
        }
    }

    resetTabs(idx);
}

function init() {
    var tabULs = document.getElementsByName("tabs_ul");
    for (var i = 0; i < tabULs.length; ++i) {
        tabLinksArr[i] = new Array();
        contentDivsArr[i] = new Array();
        initTabUL(i, tabULs[i], tabLinksArr[i], contentDivsArr[i]);
    }

    initMainTabs();
}

function showTab(element, idx) {
    var selectedId = getTabContentId(element.id);

    // Highlight the selected tab, and dim all others.
    // Also show the selected content div, and hide all others.
    for (var id in contentDivsArr[idx]) {
        if (id == selectedId) {
            tabLinksArr[idx][id].className = 'selected';
            contentDivsArr[idx][id].className = 'tabContent';
        } else {
            tabLinksArr[idx][id].className = '';
            contentDivsArr[idx][id].className = 'tabContent hide';
        }
    }
}

function getFirstChildWithTagName(element, tagName) {
    for (var i = 0; i < element.childNodes.length; i++) {
        if (element.childNodes[i].nodeName == tagName)
            return element.childNodes[i];
    }
}

function getTabContentId(tabId) {
    return tabId.substring(1);
}

function drawChart(dataset) {
    var bar = d3.select(".chart").selectAll("div").data(dataset).enter().append("div");
    bar.append("div").attr("class", "bar").style("width", function(d) {
        var barHeight = d.value * 5;
        return barHeight + "px";
    });
    bar.append("text").text(function(d) {
        return d.name;
    });
}
