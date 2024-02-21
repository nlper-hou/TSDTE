for index1 in {0..2}; do
    python main.py --K=4 --language="zh" --index=$index1
    python main.py --K=4 --language="en" --index=$index1
done
