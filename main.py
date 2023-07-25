from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForQuestionAnswering, AutoModelForCausalLM, AutoModel
from pre.downloads import download
from pre.dataset import QuestionsDataset
from post.eval import eval
from post.html_generate import generate_html_report
from post.app import app
import argparse
from huggingface_hub import snapshot_download
from tqdm import *
import os

def main(args):
    # 下载数据集
    if not os.path.exists(args.data_path):
        os.makedirs(args.data_path)
    if not download(args.data_path):
        print("download failed!")
        return
    
    # 获取模型 / 模型保存
    model_name = args.model_name
    model_type = args.model_type
    download_path = "./models/"+model_name
    load_path = model_name if not args.use_local else download_path
    if args.download:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        try:
            print("########### Start downloading. It might take a few minutes to finish. ###########")
            snapshot_download(repo_id=model_name,local_dir=download_path)
            print("########### Download finished! ###########")
        except:
            print("model error!")
            return
    try:
        tokenizer = AutoTokenizer.from_pretrained(load_path)
    except:
        print("model not found!")
        return
    try:
        if model_type == "Seq2Seq":
            model = AutoModelForSeq2SeqLM.from_pretrained(load_path)
        elif model_type == "QuesAns":
            model = AutoModelForQuestionAnswering.from_pretrained(load_path)
        elif model_type == "TextGen":
            model = AutoModelForCausalLM.from_pretrained(load_path)
        else:
            try: 
                model = AutoModel.from_pretrained(load_path)
            except:
                print("model load failed!")
            return
    except:
        print("wrong model type!")
        
    # 获取测试数据集
    test_path = args.data_path + "/bai-scieval/bai-scieval-dev.json" 
    dataset = QuestionsDataset(test_path, args)
    
    # 进行测试并记录结果
    result = []
    for i, question in tqdm(enumerate(dataset),desc="Perform model testing: "):
        response = {}
        response['id'] = question['id']
        input_ids = tokenizer(question['prompt'], return_tensors="pt", max_length=1024, truncation=True).input_ids
        outputs = model.generate(input_ids, max_new_tokens = 1000)
        response['pred'] = tokenizer.decode(outputs[0]).replace("<pad> ","").replace("</s>","")
        result.append(response)
    
    # 输出测试结果
    
    metrics = eval(result)
    print(metrics)
    generate_html_report(args, metrics)
    app.run()
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="./data", type=str)
    parser.add_argument("--model_name", default="google/flan-t5-base", type=str, help="the name of model in hugging face")
    parser.add_argument("--model_type", default="Seq2Seq", type=str, help="type of model:['Seq2Seq', 'QuesAns', 'TextGen', 'Default']")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--use_local", action="store_true")
    parser.add_argument("--category", type=str, default="all", help="choose a category: ['all', 'biology','physics','chemistry']")
    parser.add_argument("--ability", type=str, default="all", help="the focus ability of questions: ['all','Knowledge Application','Research Ability','Base Knowledge','Scientific Calculation']")
    parser.add_argument("--type", type=str, default="all", help="type of questions: ['all', 'multiple-choice','judge','filling']")

    args = parser.parse_args()
    main(args)