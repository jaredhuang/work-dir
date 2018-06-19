package com.github.ningg.mvnbook.helloworld;
import org.junit.Assert;
import org.junit.Test;
public class HelloWorldTest {
	@Test
	public void testSayHello(){
		HelloWorld helloWorld = new HelloWorld();
		String result = helloWorld.sayHello();
		Assert.assertEquals("Hello Maven", result);
	}
}
