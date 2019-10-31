import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class Multiply {
	// Mapper<input_key, input_value, output_key, output_value>
  public static class MultiMapper extends Mapper<Object, Text, Text, Text>{
		private Text all = new Text();
		private Text location = new Text();
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
				StringTokenizer itr = new StringTokenizer(value.toString());
				String [] spliter = new String [4];
				while(itr.hasMoreTokens()) {
					for (int i = 0 ; i < 4 ; i++) {
						spliter[i] = itr.nextToken();
						spliter[i] =spliter[i].replace("[","");
						spliter[i] =spliter[i].replace("]","");
						spliter[i] =spliter[i].replace(",","");
					}
					all.set(spliter[0]+" "+spliter[1]+" "+spliter[2]+" "+spliter[3]);
					for (int i = 0 ; i < 5 ; i++) {
						if(spliter[0].equals("\"a\"")) {
							location.set(spliter[1]+" "+String.valueOf(i));
							context.write(location, all);
						}
						else {
							location.set(String.valueOf(i)+" "+spliter[2]);
							context.write(location, all);
						}
					}
				}
		}
	}

  public static class MultiReducer extends Reducer<Text,Text,Text,IntWritable> {
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      int sum = 0;
			
			int [] a_array = {0,0,0,0,0};
			int [] b_array = {0,0,0,0,0};
			
			String [] val_element;
			
			for (Text val : values) {
				val_element = val.toString().trim().split(" ");
				System.out.println(val_element[0]);
				if (val_element[0].equals("\"a\""))
					a_array[Integer.parseInt(val_element[2])] += Integer.parseInt(val_element[3]);
				else
					b_array[Integer.parseInt(val_element[1])] += Integer.parseInt(val_element[3]);
			}
			
			for (int i = 0 ; i < 5 ; i++) {
				sum += a_array[i]*b_array[i]; 
			}
			
      result.set(sum);
      context.write(key, result);
    }
  }
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Multiply");
    job.setJarByClass(Multiply.class);
    job.setMapperClass(MultiMapper.class);
		job.setMapOutputValueClass(Text.class);
    // to reduce network bottleneck
    job.setReducerClass(MultiReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
