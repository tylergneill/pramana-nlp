<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />


<xsl:template match="TEI/text/body">

	<body>
	<xsl:copy-of select="./@*"/>
	<xsl:copy-of select="./head"/>

  <xsl:for-each select="./div">
		<div>

			<xsl:copy-of select="./@*"/>
			<xsl:copy-of select="./head"/>

			<div>

				<xsl:copy-of select="./@*"/>

				<xsl:for-each select=".//quote[@type='commentary1']|.//quote[@type='base-text']|.//p/quote[@type='base-text']|.//head|.//trailer|.//pb">
					<xsl:copy-of select="."/>
				</xsl:for-each>

			</div>

		</div>
  </xsl:for-each>

	</body>

</xsl:template>

</xsl:stylesheet>



<!--
<!~~
		<div>
 ~~>
		<xsl:value-of select="/TEI/text/body/div1"/>
<!~~
		<xsl:copy-of select="./@*"/>
		<xsl:copy-of select="./text()"/>
 ~~>

<!~~
		<xsl:for-each select="div">
			<div>
			<xsl:copy-of select="./@*"/>
			<xsl:copy-of select="./text()"/>

			<xsl:for-each select=".//quote[@type='commentary1']">
				 <xsl:copy-of select="."/>

			</xsl:for-each>
			</div>

		</xsl:for-each>
 ~~>

<!~~
		</div>
 ~~>

	</xsl:for-each>

</xsl:template>
 -->

<!-- </xsl:stylesheet> -->
