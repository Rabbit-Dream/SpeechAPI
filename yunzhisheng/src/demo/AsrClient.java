package demo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class AsrClient {
	//申请地址http://dev.hivoice.cn/
	public static final String appKey = "d7cqvsjiy2evpszjrlqwjz3qvwqjkorqi7o2xxat";
	public static final String secret = "d3c10b42e7f5b6404e272e2eb1327be5";
	private String mWebApiUrl;
	public AsrClient(String webApiUrl) {
		this.mWebApiUrl = webApiUrl;
	}
	public String parseAudio(String fileName) {
		String userId = "user_id";
		String deviceId = "IMEI1234567890";
		HttpURLConnection conn = null;
		FileInputStream inputStream = null;
		try {
			URL url = new URL(this.mWebApiUrl + "?appkey=" + appKey + "&userid=" + userId + "&id=" + deviceId);
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestProperty("Content-Type", "audio/x-wav;codec=pcm;bit=16;rate=16000");
			conn.setRequestProperty("Accept", "text/plain");
			conn.setRequestProperty("Accept-Language", "zh_CN");
			conn.setRequestProperty("Accept-Charset", "utf-8");
			conn.setRequestProperty("Accept-Topic", "general");
			conn.setRequestMethod("POST");
			conn.setDoInput(true);
			conn.setDoOutput(true);
			OutputStream out = conn.getOutputStream();
			byte[] buffer = new byte[640];
			inputStream = new FileInputStream(new File(fileName));
			int len = -1;
			while ((len = inputStream.read(buffer)) != -1) {
				out.write(buffer, 0, len);
			}
			inputStream.close();
			inputStream = null;
			out.flush();
			out.close();
			if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
				BufferedReader resultReader = new BufferedReader(new InputStreamReader(
						conn.getInputStream(), "utf-8"));
				String line = "";
				String result = "";
				while ((line = resultReader.readLine()) != null) {
					result += line;
				}
				resultReader.close();
				return result;
			}
			else {
				System.out.println("失败了: ResponseCode=" + conn.getResponseCode());
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {	
			if (conn != null) {
				conn.disconnect();
			}
			if (inputStream != null) {
				try {
					inputStream.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return null;
	}
	public static void main(String []args) {
		AsrClient client = new AsrClient("http://api.hivoice.cn/USCService/WebApi");
		String result = client.parseAudio("E:/Users/10178/Desktop/test/01.wav");
		if(result != null) {
			System.out.println("识别结果:\n" + result);
		}
	}
}