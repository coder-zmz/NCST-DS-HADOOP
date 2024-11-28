package com.tzjava;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private Text outK = new Text();
    private IntWritable outV = new IntWritable(1);
    private static final String STOP_WORDS_PATH = "src/main/resources/stopWords.txt";
    private Set<String> stopWordsSet;
    // 预编译正则
    private static final Pattern WORD_PATTERN = Pattern.compile(".*[a-zA-Z0-9].*");

    private Set<String> loadStopWords(String filePath) throws IOException {
        Set<String> stopWords = new HashSet<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] words = line.split(" ");
                for (String word : words) {
                    stopWords.add(word);
                }
            }
        }
        return stopWords;
    }

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        try {
            stopWordsSet = loadStopWords(STOP_WORDS_PATH);
        } catch (IOException e) {
            // 处理文件读取失败的情况
            System.err.println("Failed to load stop words: " + e.getMessage());
            stopWordsSet = new HashSet<>(); // 初始化为空集合，避免后续操作出错
        }
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        // 获取一行
        String line = value.toString();

        // 切割
        String[] words = line.split(" ");

        // 循环写出
        for (String word : words) {
            // 去除单字、标点符号
            if (word.length() <= 1) {
                continue;
            }

            // 使用正则判断是否为字母、数字等，如果为是，则continue
            if (WORD_PATTERN.matcher(word).matches()) {
                continue;
            }

            // 剔除停用词，停用词存储在stopWords.txt中
            if (stopWordsSet.contains(word)) {
                continue;
            }

            // 封装outK
            outK.set(word);
            // 写出
            context.write(outK, outV);
        }


    }
}
