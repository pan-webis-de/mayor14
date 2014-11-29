import java.io.StringReader;
import java.util.*;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.WordToSentenceProcessor;
import edu.stanford.nlp.process.Morphology;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import java.nio.file.*;
import java.io.*;


class EnglishTagger{
    MaxentTagger postagger;
	Morphology lemmatizer;

	WordToSentenceProcessor<CoreLabel> ssplit;
	TokenizerFactory<CoreLabel> tokenizer;

	public EnglishTagger(){
		this.postagger  = new MaxentTagger("edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger");
		this.lemmatizer = new Morphology();
        this.ssplit     = new WordToSentenceProcessor();
	}

    public void tag(String text, Path filepath){

		StringReader r = new StringReader(text);
        PTBTokenizer tokenizer = new PTBTokenizer(r,new CoreLabelTokenFactory(),"invertible,ptb3Escaping=true");
		List<CoreLabel> tokens = tokenizer.tokenize();

		Writer writer = null;

        try {
	            writer = new FileWriter(filepath.toString()+"_tag");
		for (List<CoreLabel> sntc: this.ssplit.process(tokens)) {
			try{
			for (TaggedWord wt:  this.postagger.tagSentence(sntc)) {
                String lemma=this.lemmatizer.lemma(wt.word(),wt.tag());
				writer.write(wt.word());
				writer.write("\t");
				writer.write(wt.tag());
				writer.write("\t");
				writer.write(lemma);
				writer.write("\n");
			}
			}catch(Exception e){
				System.out.print("Error with sentence:");
				System.out.println(sntc);
		        e.printStackTrace();
			}
		}
	    } catch (IOException e) {
		           System.err.println("Error writing the file : ");
		           e.printStackTrace();
		}

		
try {
	                    writer.close();
	                } catch (IOException e) {
	 
	                    System.err.println("Error closing the file : ");
	                    e.printStackTrace();
	                }

	}

	public static void main (String[] args) {
		EnglishTagger sp = new EnglishTagger();
		for (String s: args) {
		try{
			Files.walk(Paths.get(s)).forEach(filePath -> {
				if (Files.isRegularFile(filePath)) {
					if(filePath.toString().endsWith(".txt")){
					try{
					File file = new File(filePath.toString());
					FileInputStream fis = new FileInputStream(file);
					byte[] data = new byte[(int) file.length()];
					fis.read(data);
					fis.close();
					String str = new String(data, "UTF-8");
						System.out.println(filePath.toString());

						sp.tag(str,filePath);
					}catch(Exception e){}
				}}
			});
		}catch(Exception e){}
		}

	}

}
