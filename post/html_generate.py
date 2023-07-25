# coding:utf-8

import argparse
from dominate.tags import *
import os

style_applied = '''
        body{
			font-family: verdana,arial,sans-serif;
			font-size:11px;
		}
		table.gridtable {
			color: #333333;
			border-width: 3px;
			border-color: #666666;
			border-collapse: collapse;
            font-size:14px;
            margin-left:10%;
		}
		table.gridtable th {
			border-width: 1px;
			padding: 10px;
			border-style: solid;
			border-color: #666666;
			background-color: #DDEBF7;
		}
		table.gridtable td {
			border-width: 1px;
			padding: 8px;
			border-style: solid;
			border-color: #666666;
			background-color: #ffffff;
			text-align:center;
		}
		li {
			margin-top:5px;
		}
        div{
            margin-top:10px;
        }
        h1{
            font-size:28px;
            text-align: center;
        }
        h2{
            font-size:20px;
            margin-left:40px;
        }
    '''

def set_head(model_name:str):
    head_str = model_name.split('/')[1] + " 模型检测准确度文档"
    hello_div = div(id='hello')
    hello_div.add(h1(head_str))

def set_title(title):
    title_str = title
    title_div = div()
    title_div.add(h2(title_str))

def set_table_head():
    with tr(): # head > 能力 纵列 > 学科
        th("Category")
        th("Base Knowledge")
        th("Knowledge Application")
        th("Scientific Calculation")
        th("Research Ability")
        th("All")

def fill_table_data(category:str, base, knowledge, science, research, all):
    data_tr = tr()
    data_tr += td(category.replace(category[0],category[0].upper(),1))
    base = round(base,2) if base else "--"   
    knowledge = round(knowledge,2) if knowledge else "--"   
    science = round(science,2) if science else "--"   
    research = round(research,2) if research else "--"   
    all = round(all,2)
    data_tr += td(base)
    data_tr += td(knowledge)
    data_tr += td(science)
    data_tr += td(research)
    data_tr += td(all)

def generate_result_table(metrics:dict):
    result_div = div(id='test result')    
    with result_div.add(table(cls='gridtable')).add(tbody()):
        set_table_head()
        for key in ['physics','chemistry','biology','all']:
            all = metrics[key].get('all')
            if not all:
                continue
            base = metrics[key].get('Base Knowledge')
            knowledge = metrics[key].get('Knowledge Application')
            science = metrics[key].get('Scientific Calculation')
            research = metrics[key].get('Research Ability')
            fill_table_data(key,base,knowledge,science,research,all) 

def generate_pic_script(metrics):
    table = []
    for i in ['all','Base Knowledge', 'Knowledge Application','Scientific Calculation', 'Research Ability']:
        row = []
        for j in ['all','physics','chemistry','biology']:
            v = metrics.get(j)
            if v:
                v = v.get(i)
                if v:
                    v *= 100
                else: v = "--"
            else: v = "--"
            row.append(v)
        table.append(row)
    
    div(id="main", style="width:80%;height:400px;margin: 0 auto")
    div(id="main2", style="width:80%;height:400px;margin: 0 auto")
    script(src="http://echarts.baidu.com/build/dist/echarts.js")
    script("""
           // 路径配置
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });

        // 使用
        require(
            [
                'echarts',
                'echarts/chart/radar', // 使用柱状图就加载bar模块，按需加载
                'echarts/chart/bar',
                'echarts/chart/line'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('main'));
                var myChart2 = ec.init(document.getElementById('main2'));

                var option = { //具体细节的描述
    tooltip: {
        trigger: 'axis'
    },
    grid: {
        width: '80%'
    },
    legend: {
        data: ['All', 'Base Knowledge', 'Knowledge Application', 'Scientific Calculation', 'Research Ability'],
        y: 'bottom',
        x: 'right',
        orient: 'vertical'
    },
    toolbox: {
        show: true,
        feature: {
            mark: {
                show: true
            },
            dataView: {
                show: true,
                readOnly: true
            },
            magicType: {
                show: false,
                type: ['line', 'bar']
            },
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
    calculable: true,
    xAxis: [
        {
            type: 'category',
            data: ['All', 'Physics', 'Chemistry', 'Biology']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '准确率（%）'
        }
    ],
    series: [
        {
            name: 'All',
            type: 'bar',
            data: 
                """
                +str(table[0])+
                """
        },
        {
            name: 'Base Knowledge',
            type: 'bar',
            data: 
                """
                +str(table[1])+
                """
        },
        {
            type: 'bar',
            name: 'Knowledge Application',
            data: 
                """
                +str(table[2])+
                """
        },
        {
            type: 'bar',
            name: 'Scientific Calculation',
            data: 
                """
                +str(table[3])+
                """
        },
        {
            type: 'bar',
            name: 'Research Ability',
            data: 
                """
                +str(table[4])+
                """
        }
    ],
    title: {
        text: '各学科各能力准确度'
    }
                };

                var option2 = {
                    title: {
                        text: '各学科能力对比'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        orient: 'vertical',
                        x: 'right',
                        y: 'bottom',
                        data: ['All', 'Physics', 'Chemistry', 'Biology']
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {
                                show: true
                            },
                            dataView: {
                                show: true,
                                readOnly: false
                            },
                            restore: {
                                show: true
                            },
                            saveAsImage: {
                                show: true
                            }
                        }
                    },
                    polar: [
                        {
                            indicator: [
                                {
                                    text: 'Base Knowledge',
                                    min: 0,
                                    max: 100
                                },
                                {
                                    text: 'Knowledge Application',
                                    min: 0,
                                    max: 100
                                },
                                {
                                    text: 'Scientific Calculation',
                                    min: 0,
                                    max: 100
                                },
                                {
                                    text: 'Research Ability',
                                    min: 0,
                                    max: 100
                                }
                            ]
                        }
                    ],
                    calculable: true,
                    series: [
                        {
                            name: '',
                            type: 'radar',
                            data: [
                                {
                                    value: """
                                    +str([row[0] for row in table[1:]])+
                                    """,
                                    name: 'All'
                                }
                            ]
                        },
                        {
                            name: '',
                            type: 'radar',
                            data: [
                                {
                                    value: """
                                    +str([row[1] for row in table[1:]])+
                                    """,
                                    name: 'Physics'
                                }
                            ]
                        },
                        {
                            type: 'radar',
                            name: '',
                            data: [
                                {
                                    value: """
                                    +str([row[2] for row in table[1:]])+
                                    """,
                                    name: 'Chemistry'
                                }
                            ]
                        },
                        {
                            type: 'radar',
                            name: '',
                            data: [
                                {
                                    value: """
                                    +str([row[3] for row in table[1:]])+
                                    """,
                                    name: 'Biology'
                                }
                            ]
                        }
                    ]
                };



                // 为echarts对象加载数据 
                myChart.setOption(option);
                myChart2.setOption(option2);
            }
        );
           """)

def generate_html_report(args, metrics):
    html_root = html()
    # html head
    with html_root.add(head()):
         title("report")
         style(style_applied, type='text/css')
         meta(charset = "utf-8")
    # html body
    with html_root.add(body()):
        set_head(args.model_name)
        set_title("模型准确度数据（保留两位小数）")
        generate_result_table(metrics)
        br()
        set_title("相关图表")
        generate_pic_script(metrics)
    # save as html file
    file_path = './post/templates/'
    if not os.path.isdir(file_path):
        file_path = './templates/'
    file_path += 'report.html'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_root.render())    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="./data", type=str)
    parser.add_argument("--model_name", default="google/flan-t5-base", type=str, help="the name of model in hugging face")
    parser.add_argument("--model_type", default="Seq2Seq", type=str, help="type of model")
    parser.add_argument("--download", action="store_true", help="download the model to local")
    parser.add_argument("--use_local", action="store_true", help="use local model")
    parser.add_argument("--category", type=str, default="all", help="choose a category: ['all', 'biology','physics','chemistry']")
    parser.add_argument("--ability", type=str, default="all", help="the focus ability of questions: ['all','Knowledge Application','Research Ability','Base Knowledge','Scientific Calculation']")
    parser.add_argument("--type", type=str, default="all", help="type of questions: ['all', 'multiple-choice','judge','filling']")

    metrics = {'biology': {'Base Knowledge': 0.6, 'Knowledge Application': 0.5, 'Scientific Calculation': 0.2, 'all': 0.45}, 'chemistry': {'Base Knowledge': 1.0, 'all': 1.0}, 'physics': {}, 'all': {'Base Knowledge': 0.6666666666666666, 'Knowledge Application': 0.5, 'Scientific Calculation': 0.2, 'all': 0.47619047619047616}}
    args = parser.parse_args()
    generate_html_report(args, metrics)
